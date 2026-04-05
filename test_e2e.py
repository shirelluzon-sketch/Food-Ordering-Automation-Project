from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time
import pytest
import re


users_list = [["verdek@kgmail.com", "luies123c4554"],["bener@gmail.com","kikjghi52p21"],["shoshan@gmail.com","nachtpigsik88ke3113321"]]
@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    driver.get("https://svburger1.co.il/#/HomePage")
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.close()

def move_to_and_click(driver, xpath):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    element.click()

@pytest.mark.sanity
def test_sanity(setup):
    driver = setup


    driver.find_element(By.XPATH, "//a[@href='#/SignIn']/button").click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shirelluzon1@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel123#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//h5[text()="Combo Meal"]'))
    ).click()

    move_to_and_click(driver, '//button[normalize-space()="Reserve"]')


    move_to_and_click(driver, '//button[normalize-space()="Send"]')


    total_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            '//*[contains(translate(text(),"abcdefghijklmnopqrstuvwxyz","ABCDEFGHIJKLMNOPQRSTUVWXYZ"), "TOTAL")]'
        ))
    )

    total_text = total_div.text
    print("Text from the website:", total_text)

    match = re.search(r'([\d\.]+)', total_text)
    if match:
        total_value = float(match.group(1))
    else:
        raise Exception("No total amount found on the page")

    expected_total = 64.9

    assert total_value == expected_total, (
        f"❌ Wrong total! Actual: {total_value}$ | Expected: {expected_total}$"
    )
    print(f"✅ Correct total: {total_value}$")


def test_sign_in_via_gmail_mail (setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shirelluzon1@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel123#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()= "Combo Meal"]').click()

    time.sleep(2)

    move_to_and_click(driver, '//button[normalize-space()="Reserve"]')

    time.sleep(4)

    driver.find_element(By.XPATH, '//button[normalize-space()="Send"]').click()

    time.sleep(3)

def test_sign_in_via_yahoo_mail (setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shir@yahoo.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shir1234!")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()= "Kids Meal"]').click()

    time.sleep(2)

    move_to_and_click(driver, '//button[normalize-space()="Reserve"]')

    time.sleep(4)

    driver.find_element(By.XPATH, '//button[normalize-space()="Send"]').click()

    time.sleep(3)


def test_EH_Login_without_insert_an_Email(setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()

    password_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]')
    password_input.send_keys("shir1234!")

    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(1)
    try:
        error_msg = driver.find_element(By.XPATH, '//div[contains(text(),"Failed to log in")]')
        assert "Failed to log in" in error_msg.text
    except:
        email_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]')
        assert email_input.get_attribute("value") == "", "Email field should be empty"

def test_EH_Login_with_wrong_password (setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("sshirelluzon1@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("1234567")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        assert "Failed to log in" in alert.text
        alert.accept()
    except:
        error_msg = driver.find_element(By.XPATH, '//div[contains(text(),"Failed to log in")]')
        assert "Failed to log in" in error_msg.text


@pytest.mark.parametrize("anything", users_list)

def test_sign_up (setup, anything):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    driver.find_element(By.XPATH, '// form / input[1]').send_keys("david")
    driver.find_element(By.XPATH, '// form / input[2]').send_keys("eliron")
    driver.find_element(By.XPATH, '// form / input[3]').send_keys(anything[0])
    driver.find_element(By.XPATH, '// form / input[4]').send_keys(anything[1])
    driver.find_element(By.XPATH, '// form / input[5]').send_keys(anything[1])
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    time.sleep(2)

def test_sign_up_only_with_required_Fields (setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("sivan96@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys("svsvsvp")
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys("svsvsvp")
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    time.sleep(3)



def test_sign_up_only_with_a_First_name_that_contains_7_chars (setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys("shloooo")
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys("peretz")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shlomit88@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys("sh121212")
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys("sh121212")
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    time.sleep(3)


def test_BV_Sign_Up_with_10_characters_on_first_name (setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys("danieledri")
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys("amzaleg")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("danielam888@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys("sh121212")
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys("sh121212")
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    time.sleep(3)


def test_BV_Sign_Up_with_10_characters_on_last_name (setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys("dani")
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys("edriedried")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("danielam100@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys("sh121212")
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys("sh121212")
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    time.sleep(3)




def test_EH_sign_up_with_a_first_name_in_Hebrew_ (setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys("שיראל")
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys("luzon")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shirelii@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys("sl121212")
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys("sl121212")
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    time.sleep(2)
    alert = driver.switch_to.alert
    assert "First name must be in English letters only" in alert.text
    alert.accept()


def test_EH_sign_up_with_Password_shorter_than_6_characters_ (setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys("dana")
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys("choen")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("dana26@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys("1234")
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys("1234")
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    time.sleep(2)
    alert = driver.switch_to.alert
    assert "Password should be at least 6 characters" in alert.text
    alert.accept()

def test_EH_Sign_Up_with_different_password_on_Confirm_Password (setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Type your first name"]').send_keys("lorena")
    driver.find_element(By.XPATH, '//input[@placeholder="Type your last name"]').send_keys("lomim")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("loren77@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Create Password"]').send_keys("987654")
    driver.find_element(By.XPATH, '//input[@placeholder="Confirm Password"]').send_keys("98765")
    driver.find_element(By.XPATH, '//button[text() ="Sign Up"]').click()
    time.sleep(2)
    alert = driver.switch_to.alert
    assert "password and confirm error" in alert.text
    alert.accept()

def test_Reservation_and_confirm_reservation_Functionality_order_2_meals (setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shirelluzon2@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel1234#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()= "Combo Meal"]').click()

    time.sleep(2)

    move_to_and_click(driver, '//button[normalize-space()="Reserve"]')

    time.sleep(4)

    driver.find_element(By.XPATH, '//input[@type="number"]').clear()
    driver.find_element(By.XPATH, '//input[@type="number"]').send_keys("2")

    time.sleep(3)

    driver.find_element(By.XPATH, '//button[normalize-space()="Send"]').click()

    time.sleep(3)
    total_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            '//*[contains(translate(text(),"abcdefghijklmnopqrstuvwxyz","ABCDEFGHIJKLMNOPQRSTUVWXYZ"), "TOTAL")]'
        ))
    )
    total_text = total_div.text
    print("Text from the website:", total_text)


    match = re.search(r'([\d\.]+)', total_text)
    if match:
        total_value = float(match.group(1))
    else:
        raise Exception("No total amount found on the summary page")

    expected_total = 129.8
    assert total_value == expected_total, (
        f"❌ SYSTEM ERROR: Wrong total! Actual: {total_value}$ | Expected: {expected_total}$"
    )
    print(f"✅ Correct total: {total_value}$")


def test_Reservation_and_confirm_reservation_Functionality_Select_same_meal_twice_to_cancel_order (setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shirelluzon2@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel1234#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.XPATH, '//h5[text()= "Combo Meal"]').click()

    time.sleep(2)
    driver.find_element(By.XPATH, '//h5[text()= "Combo Meal"]').click()
    time.sleep(2)




def test_Reservation_and_confirm_reservation_Functionality_press_on_Log_out (setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shirelluzon2@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel1234#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@variant="link"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", logout_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", logout_button)

    time.sleep(2)




def move_to_and_click(driver, xpath):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.execute_script("arguments[0].click();", element)


def test_Reservation_and_confirm_reservation_Bv_Order_3_meals(setup):
    driver = setup

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@href="#/SignIn"]/button'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Enter your email"]'))
    ).send_keys("shirelluzon2@gmail.com")

    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel1234#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//h5[text()="Combo Meal"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//h5[text()="Burger"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//h5[text()="Vegan"]'))
    ).click()

    move_to_and_click(driver, '//button[normalize-space()="Reserve"]')
    move_to_and_click(driver, '//button[normalize-space()="Send"]')

    subtotal_element = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Total:")]'))
    )
    subtotal_text = subtotal_element.text.strip()
    subtotal_value = float(subtotal_text.replace('Total:', '').replace('$', '').strip())

    print(f"Total In the summary screen: {subtotal_value}")

    expected_total = 163.9
    assert subtotal_value == expected_total, \
        f"ERROR: The summary screen appeared {subtotal_value}, should be {expected_total}"

    confirmation_element = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Total:")]'))
    )
    confirmation_text = confirmation_element.text.strip()
    confirmation_value = float(confirmation_text.replace('Total:', '').replace('$', '').strip())

    print(f"Total on the confirmation screen: {confirmation_value}")

    assert subtotal_value == confirmation_value, \
        f"A bug was found ❌ : In the summary screen {subtotal_value}, on the confirmation screen {confirmation_value}"





def test_Functionality_order_two_meals(setup):
    driver = setup


    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shirelluzon2@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel1234#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//h5[text()="Kids Meal"]'))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//h5[text()="Burger"]'))
    ).click()


    reserve_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//button[normalize-space()="Reserve"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reserve_button)
    time.sleep(3)
    reserve_button.click()


    send_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Send"]'))
    )


    subtotal_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Total") or contains(text(),"Subtotal")]'))
    )
    subtotal_text = subtotal_element.text.strip()
    subtotal_value = float(subtotal_text.replace('Subtotal:', '').replace('Total:', '').replace('$', '').strip())
    print(f"Displayed Total/Subtotal: {subtotal_value}")


    expected_subtotal = 114.4


    if subtotal_value != expected_subtotal:
        print(f"ERROR: System shows {subtotal_value} but expected {expected_subtotal}")
    assert subtotal_value == expected_subtotal, f"Subtotal mismatch! Displayed: {subtotal_value}, Expected: {expected_subtotal}"


    send_button.click()
    time.sleep(1)

def move_to_and_click_safe(driver, xpath):
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    try:
        element.click()
    except:
        ActionChains(driver).move_to_element(element).click().perform()





def test_EH_Insert_3_on_quantity_kids_meal(setup):
    driver = setup


    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shir@yahoo.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shir1234!")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//h5[text()= "Kids Meal"]'))
    ).click()


    move_to_and_click_safe(driver, '//button[normalize-space()="Reserve"]')
    time.sleep(2)


    quantity_input = driver.find_element(By.XPATH, '//input[@type="number"]')
    quantity_input.clear()
    quantity_input.send_keys("3")
    time.sleep(1)


    move_to_and_click_safe(driver, '//button[normalize-space()="Send"]')


    expected_total = 128.7
    subtotal_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Total") or contains(text(),"Subtotal")]'))
    )


    WebDriverWait(driver, 10).until(
        lambda d: float(subtotal_element.text.replace('Subtotal:', '').replace('Total:', '').replace('$', '').strip()) == expected_total
    )

    subtotal_text = subtotal_element.text.strip()
    subtotal_value = float(subtotal_text.replace('Subtotal:', '').replace('Total:', '').replace('$', '').strip())
    print(f"Displayed Total/Subtotal: {subtotal_value}")

    assert subtotal_value == expected_total, f"Total mismatch! Displayed: {subtotal_value}, Expected: {expected_total}"


def test_EH_Select_4_meal (setup):
    driver = setup


    driver.find_element(By.XPATH, '//a[@href="#/SignIn"]/button').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your email"]').send_keys("shirelluzon1@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel123#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)


    meals = ["Combo Meal", "Burger", "Vegan", "Kids Meal"]
    for meal in meals:
        driver.find_element(By.XPATH, f'//h5[text()="{meal}"]').click()
        time.sleep(1)


    move_to_and_click(driver, '//button[normalize-space()="Reserve"]')
    time.sleep(2)


    move_to_and_click(driver, '//button[normalize-space()="Send"]')
    time.sleep(2)


    subtotal_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Total") or contains(text(),"Subtotal")]'))
    )
    subtotal_text = subtotal_element.text.strip()
    subtotal_value = float(subtotal_text.replace('Subtotal:', '').replace('Total:', '').replace('$', '').strip())
    print(f"Displayed Total/Subtotal: {subtotal_value}")


    expected_subtotal_for_3_meals = 117.0


    if subtotal_value == expected_subtotal_for_3_meals:
        print("System automatically limited the order to 3 meals.")
    else:
        print("ERROR: Subtotal does not match 3 meals! Actual:", subtotal_value)
        assert False, f"Total mismatch! Displayed: {subtotal_value}, Expected: {expected_subtotal_for_3_meals}"



@pytest.mark.functional
def test_functional_order_one_meal(setup):
    driver = setup


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@href="#/SignIn"]/button'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Enter your email"]'))
    ).send_keys("shirelluzon1@gmail.com")

    driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys("shirel123#")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()




    move_to_and_click(driver, '//h5[text()="Combo Meal"]')




    move_to_and_click(driver, '//button[normalize-space()="Reserve"]')




    table_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, '//label[normalize-space()="Table No."]/following::input[@type="number"][1]')
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", table_input)
    table_input.clear()
    table_input.send_keys("2")




    move_to_and_click(driver, '//button[normalize-space()="Send"]')




    total_price = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h3[contains(@class,"total-price")]'))
    ).text

    assert "64.9" in total_price, f"error – I expected ל־64.9, I actually got it {total_price}"