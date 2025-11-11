from ldap3 import Server, Connection, ALL, NTLM, core

LDAP_SERVER = "192.168.56.101"
DOMAIN = "IFTS"
USERNAME = "IFTS\\Administrator"   # ⚠️ reemplazá con tu usuario AD real
PASSWORD = "IFTS.2025"          # ⚠️ reemplazá con la contraseña real

try:
    print("🔄 Intentando conectar con el servidor LDAP...")
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=USERNAME, password=PASSWORD, authentication=NTLM, auto_bind=True)
    print("✅ Conexión exitosa:", conn.bound)
    conn.unbind()
except core.exceptions.LDAPBindError as e:
    print("❌ Error de credenciales o usuario:", e)
except core.exceptions.LDAPSocketOpenError as e:
    print("❌ No se puede conectar al servidor LDAP:", e)
except Exception as e:
    print("⚠️ Error inesperado:", e)