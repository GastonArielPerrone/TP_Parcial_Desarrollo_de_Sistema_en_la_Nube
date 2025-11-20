import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from ldap3 import Server, Connection, ALL, NTLM, core
from django.conf import settings

logger = logging.getLogger(__name__)

class ActiveDirectoryBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not password:
            return None

        try:
            server = Server(settings.LDAP_HOST, get_info=ALL)
            user_dn = f"{settings.LDAP_DOMAIN}\\{username}"
            logger.info(f"Attempting to bind with user_dn: {user_dn}")
            conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)
            
            if not conn.bound:
                logger.warning(f"LDAP bind failed for user {username}")
                return None

            logger.info(f"LDAP bind successful for user {username}")

            search_base = "dc=" + ",dc=".join(settings.LDAP_DOMAIN.lower().split('.')) + ",dc=local"
            logger.info(f"LDAP search base: {search_base}")
            search_filter = f"(sAMAccountName={username})"
            
            conn.search(search_base, search_filter, attributes=['sAMAccountName', 'givenName', 'sn', 'mail', 'telephoneNumber', 'title', 'memberOf'])

            if not conn.entries:
                logger.warning(f"LDAP user {username} not found in search.")
                return None

            entry = conn.entries[0]
            logger.info(f"LDAP user {username} found: {entry.entry_dn}")
            
            # Group membership check
            required_groups = getattr(settings, 'LDAP_REQUIRED_GROUPS', [])
            if not required_groups:
                logger.warning("LDAP_REQUIRED_GROUPS is not defined or empty in settings. Denying login as a security precaution.")
                return None

            user_groups = entry.memberOf.values if 'memberOf' in entry and entry.memberOf.values else []
            is_member = False
            for group_dn in user_groups:
                # Extracts the CN from the group DN. E.g., from "CN=Users,DC=ifts,DC=local" extracts "Users"
                # This is a simple parser; more complex DNs might need a more robust library
                try:
                    cn_part = group_dn.split(',')[0]
                    group_name = cn_part.split('=')[1]
                    if group_name in required_groups:
                        is_member = True
                        logger.info(f"User {username} is a member of required group: {group_name}")
                        break
                except IndexError:
                    logger.warning(f"Could not parse group DN: {group_dn}")

            if not is_member:
                logger.warning(f"User {username} is not in any of the required LDAP groups: {required_groups}. Access denied.")
                return None

            user_model = get_user_model()
            
            try:
                user = user_model.objects.get(dni=username)
                logger.info(f"User {username} found in local database.")
            except user_model.DoesNotExist:
                user = user_model(dni=username)
                logger.info(f"User {username} not found in local database, creating new user.")

            user.nombre = entry.givenName.value if entry.givenName else ''
            user.apellido = entry.sn.value if entry.sn else ''
            user.email = entry.mail.value if entry.mail else ''
            user.telefono = entry.telephoneNumber.value if entry.telephoneNumber else ''
            user.cargo = entry.title.value if entry.title else ''
            
            if user.pk is None:
                user.set_unusable_password()

            user.is_staff = True
            user.is_active = True
            user.save()
            logger.info(f"User {username} saved successfully.")
            
            return user

        except core.exceptions.LDAPBindError as e:
            logger.error(f"LDAP Bind Error for user {username}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during LDAP authentication for user {username}: {e}", exc_info=True)
            return None
        finally:
            if 'conn' in locals() and conn.bound:
                conn.unbind()
                logger.info(f"LDAP connection for user {username} unbound.")

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
