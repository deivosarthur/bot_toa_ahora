from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import DOWNLOAD_PATH
import time
from bot_state import BOT_STATE
from heartbeat import guardar_estado

def validar_timeout_login(inicio_login, limite=120):

    tiempo = time.time() - inicio_login
    

    if tiempo > limite:

        raise Exception(
            "⏰ Timeout login Microsoft/Oracle"
        )

        
        
        
def iniciar_sesion():
    
    BOT_STATE["estado"] = "LOGIN"

    BOT_STATE["mensaje"] = (
        "Autenticando Oracle/Microsoft"
    )

    guardar_estado()
    inicio_login = time.time()
    chrome_options = Options()
    chrome_options.add_argument(
        "--user-data-dir=C:\\selenium_profiles\\toa"
    )
    chrome_options.add_argument(
    "--safebrowsing-disable-download-protection"
    )   
    chrome_options.add_argument(
    "--disable-features=DownloadBubble"
    )

    chrome_options.add_argument(
        "--disable-features=DownloadBubbleV2"
    )

    chrome_options.add_argument(
        "--disable-notifications"
    )

    prefs = {

        "download.default_directory": DOWNLOAD_PATH,

        "download.prompt_for_download": False,

        "download.directory_upgrade": True,

        "safebrowsing.enabled": False,

        "safebrowsing.disable_download_protection": True,

        "profile.default_content_setting_values.automatic_downloads": 1
    }

    chrome_options.add_experimental_option("prefs", prefs)


    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    print(
        "PID CHROMEDRIVER:",
        driver.service.process.pid
    )
    print("PID CHROMED:",driver.capabilities)

    wait = WebDriverWait(driver, 30)

    driver.get("https://vtr.fs.ocs.oraclecloud.com/")

    print("🔹 Paso 1: Click SSO")
    validar_timeout_login(inicio_login)
    # PASO 1: BOTON SSO -------------------------------------------------------
    sso_btn = wait.until(EC.element_to_be_clickable((By.ID, "sign-in-with-sso")))
    if time.time() - inicio_login > 120:
        raise Exception("⏰ Timeout login")
    sso_btn.click()
   
    print("🔹 Paso 2: Ingresar usuario")

    # PASO 2: USUARIO -------------------------------------------------------
    print("🔹 Paso 2: Ingresar usuario (modo Oracle JET)")
    validar_timeout_login(inicio_login)
    user_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "sso_username"))
    )

    # setear valor vía JS (clave)
    driver.execute_script("""
    arguments[0].value = 'asantibaezr';
    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, user_input)

    print("✔ Usuario seteado via JS")

    # esperar que botón se habilite
    continue_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "continue-with-sso"))
    )

    continue_btn.click()

    print("✔ Click continuar SSO")

    # PASO 3: CUENTA MICROSOFT -------------------------------------------------------
    print("🔹 Paso 3: Seleccionar cuenta Microsoft")
    validar_timeout_login(inicio_login)
    try:
        account = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@data-test-id,'asantibaezr')]")
        ))
        account.click()
        print("✔ Cuenta seleccionada")
    except:
        print("⚠️ No apareció selección de cuenta")

    # PASO 4: LOGIN -------------------------------------------------------
    print("🔹 Paso 4: Login Microsoft")
    validar_timeout_login(inicio_login)
    try:
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
        login_btn.click()
        print("✔ Click iniciar sesión")
    except:
        print("⚠️ Auto-login o no requerido")

    print("🔹 Paso 4: Ingresar contraseña")
    validar_timeout_login(inicio_login)
    try:
        password_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "i0118"))
        )

        password_input.send_keys("c!5R-cldRi1R")

        print("✔ Contraseña ingresada")

        login_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        login_btn.click()

        print("✔ Click iniciar sesión")
        
    except:
        print("⚠️ No apareció input de contraseña (posible sesión guardada)")

    
    BOT_STATE["mensaje"] = (
        "Esperando respuesta Microsoft"
    )

    guardar_estado()
    # PASO 5: MANTENER SESIÓN (SI) -------------------------------------------------------
    print("🔹 Paso 5: Mantener sesión")
    validar_timeout_login(inicio_login)
    try:
        yes_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Sí'] | //button[contains(.,'Sí')]"))
        )
        yes_btn.click()
        print("✔ Sesión mantenida")
    except:
        print("⚠️ No apareció 'Mantener sesión'")

    
    BOT_STATE["mensaje"] = (
        "Validando acceso Oracle"
    )

    guardar_estado()
    # VALIDAR LOGIN REAL -------------------------------------------------------
    print("🔹 Validando entrada al sistema...")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "edt-root"))
    )

    print("✅ LOGIN COMPLETO Y FUNCIONANDO")

    return driver