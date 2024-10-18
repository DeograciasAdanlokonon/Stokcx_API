from flask import Flask, jsonify, request, render_template, make_response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize our API via FLASK app
app = Flask(__name__)


def stockx_search(reference):
    """Takes the reference of a product, search it on stockx.com and return a result"""

    url = f"https://stockx.com/search?s={reference}"

    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Required in some environments
    options.add_argument("--disable-dev-shm-usage")  # Avoid /dev/shm issues
    options.add_argument("--disable-gpu")  # Disable GPU (often unnecessary in headless)
    options.add_argument("--disable-extensions")  # Avoid issues with extensions

    driver = webdriver.Chrome(options=options)
    driver.get(url=url)

    # fetch for the first article
    article = driver.find_element(By.CSS_SELECTOR, value="#product-results a")

    # article name
    article_name = article.text.split("\n")[0]
    article_price = article.text.split("\n")[2]

    # image link
    image = article.find_element(By.CSS_SELECTOR, value="img")
    image_link = image.get_attribute("srcset").split(",")[0]

    # final result into a dictionary
    result = {
        "name": article_name,
        "price": int(article_price.replace("$", "")),
        "image": image_link.split(" ")[0]
    }

    # close driver
    driver.quit()

    # return finale result
    return result


@app.route('/')
def home():
    """Blank index for the api"""
    return render_template('index.html')


@app.route('/api', methods=['GET', 'POST'])
def api_core():
    """Take parameter reference and call the function stockx_search"""

    try:
        if request.method == 'POST':
            reference = request.form.get('reference')
            if reference:
                result = stockx_search(reference)
                if result:
                    response = make_response(jsonify({"response": {"result": result}}), 200)
                    response.headers[
                        'Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
                    response.headers['Pragma'] = 'no-cache'
                    response.headers['Expires'] = '0'
                    return response
                else:
                    return jsonify({"response": {"result": "No result found for this reference on Stockx.com"}})
            else:
                return jsonify({"response": {"error": "No product reference provided."}}), 404
        else:
            return jsonify({"response": {"error": "Method Not Allowed"}}), 405
    except Exception as e:
        return jsonify({"response": {"error": str(e)}}), 400


if __name__ == "__main__":
    # run app in debug mode to auto-load our server
    app.run(debug=True, host='0.0.0.0')

