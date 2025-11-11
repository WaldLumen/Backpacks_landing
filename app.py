from flask import Flask, render_template
import xml.etree.ElementTree as ET

app = Flask(__name__)

def load_catalog(path="static/catalog.xml"):
    tree = ET.parse(path)
    root = tree.getroot()

    shop = root.find("shop")
    if shop is None:
        return []

    categories = {}
    for cat in shop.findall("./categories/category"):
        cid = cat.get("id")
        name = cat.text
        categories[cid] = name

    offers = []
    for offer in shop.findall("./offers/offer"):
        name = offer.findtext("name")
        category_id = offer.findtext("categoryId")
        category_name = categories.get(category_id, "Без категории")
        price_text = offer.findtext("price") or ""
        try:
            price = float(price_text) if price_text != "" else None
        except ValueError:
            price = None
        oldprice_text = offer.findtext("oldprice") or ""
        try:
            oldprice = float(oldprice_text) if oldprice_text != "" else None
        except ValueError:
            oldprice = None

        pictures = [p.text for p in offer.findall("picture")]
        offers.append({
            "name": name,
            "category": category_name,
            "pictures": pictures,
            "price": price
        })

    return offers

@app.route("/")
def index():
    products = load_catalog()
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
