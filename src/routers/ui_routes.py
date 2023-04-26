# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from fastapi import APIRouter, Request, status, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session


import app
from src import schemas
from src.config import settings
import http3
import stripe
import json
from src.database.models import StoreModel, BookModel, CategoryModel, AuthorModel, UserModel, OrderItemModel, \
    OrderModel, AddressModel
from src.database.session import get_db, SessionLocal

router = APIRouter(
    tags=['User Interface']
)

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "../templates"))

# Stripe Credentials
stripe_keys = {
    "secret_key": settings.stripe_secret_key,
    "publishable_key": settings.stripe_publishable_key,
    "endpoint_secret": settings.stripe_secret_key
}


@router.get("/", status_code=status.HTTP_200_OK)
async def index(request: Request, session: SessionLocal = Depends(get_db)):
    list_category = session.query(CategoryModel).all()
    list_author = session.query(AuthorModel).all()
    list_stores = session.query(StoreModel).all()
    context = {
        "request": request,
        "categories": list_category,
        "authors": list_author,
        "stores": list_stores,
    }
    if request.session.get("user_id"):
        user = session.query(UserModel).get(request.session.get("user_id"))
        context.update({"user": user})
    return TEMPLATES.TemplateResponse("pages/index.html", context)


@router.get("/products/", status_code=status.HTTP_200_OK)
async def products_index(request: Request, response_model=HTMLResponse):
    featured_product_slug = 'featured'
    base_url = request.base_url
    product_url = app.product_router.url_path_for("get_product_by_slug", slug=featured_product_slug)
    request_url = base_url.__str__() + product_url.__str__()[1:]

    http3client = http3.AsyncClient()
    response = await http3client.get(request_url)

    featured_product = response.json()

    products_url = app.product_router.url_path_for("get_products")
    request_url2 = base_url.__str__() + products_url.__str__()[1:]

    http3client = http3.AsyncClient()
    response = await http3client.get(request_url2)

    products = response.json()
    for i, product in enumerate(products):
        if (product['slug'] == featured_product_slug):
            del products[i]

    access_key = request.cookies.get('Stripe-Account')

    if (access_key):
        # print ('here is where we can determine if local products or stripe products get loaded')
        stripe.api_key = access_key
        # stripe.

        json_data = []
        products = stripe.Product.list(expand=['data.default_price'])
        print('\n\n')
        print(products)
        print('\n\n')
        productdict = []
        for product in products:
            dict = {}
            dict['id'] = product['id']
            dict['name'] = product['name']
            dict['price'] = product["default_price"]["unit_amount"] / 100
            dict['currency'] = product["default_price"]["currency"]
            dict['full_description'] = product["description"]
            dict['info'] = product["description"][0:30]

            for index, image in enumerate(product['images']):
                dict['img_main'] = image

            dict['img_card'] = ''
            dict['img_1'] = ''
            dict['img_2'] = ''
            dict['img_3'] = ''

            productdict.append(dict)

        for product in productdict:
            json_product = json.dumps(product, indent=4, separators=(',', ': '))
            json_data.append(json_product)

    return TEMPLATES.TemplateResponse("ecommerce/index.html", {
        "request": request,
        "featured_product": featured_product,
        "products": products,
    })




@router.get("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return stripe_config


@router.get("/success")
def success(request: Request):
    return TEMPLATES.TemplateResponse("ecommerce/payment-success.html", {
        "request": request,
        "config": settings
    })


@router.get("/cancelled")
def cancelled(request: Request):
    return TEMPLATES.TemplateResponse("ecommerce/payment-cancelled.html", {
        "request": request,
        "config": settings
    })


@router.get("/create-checkout-session/{path}/")
async def create_checkout_session(path, request: Request):
    base_url = request.base_url
    product_url = app.product_router.url_path_for("get_product_by_slug", slug=path)
    request_url = base_url.__str__() + product_url.__str__()[1:]

    http3client = http3.AsyncClient()
    response = await http3client.get(request_url)

    product = response.json()

    domain_url = settings.server_address
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 100,
                        'product_data': {
                            'name': product['name'],
                            'description': 'Comfortable cotton t-shirt',
                            'images': ['https://example.com/t-shirt.png'],
                        }
                    },
                    'quantity': 1
                }
            ]
        )
        return {"sessionId": checkout_session["id"]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='There was an error with the stripe session')


# @router.get("/success")
# def success(request: Request):
#     return TEMPLATES.TemplateResponse("ecommerce/payment-success.html", {
#         "request": request,
#         "config": settings
#     })


@router.get("/presentation")
def presentation(request: Request):
    return TEMPLATES.TemplateResponse("pages/presentation.html", {
        "request": request,
        "config": settings
    })


@router.get("/page-about-us")
def page_about_us(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-about-us.html", {
        "request": request,
        "config": settings
    })


@router.get('/page-contact-us')
def page_contact_us(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-contact-us.html", {
        "request": request,
        "config": settings
    })


@router.get('/page-author')
def page_author(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-author.html", {
        "request": request,
        "config": settings
    })


@router.get('/page-sign-in')
def page_sign_in(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-sign-in.html", {
        "request": request,
        "config": settings
    })


@router.get('/page-sign-up')
def page_sign_up(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-sign-up.html", {
        "request": request,
        "config": settings
    })


@router.get('/page-address')
def page_sign_up(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-address.html", {
        "request": request,
        "config": settings
    })


@router.get('/page-404')
def page_404(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-404.html", {
        "request": request,
        "config": settings
    })


@router.get('/page-sections-hero-sections')
def page_sections_hero_sections(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-sections-hero-sections.html", {
        "request": request,
        "config": settings
    })


@router.get('/page-sections-features')
def page_sections_features(request: Request):
    return TEMPLATES.TemplateResponse("pages/page-sections-features.html", {
        "request": request,
        "config": settings
    })


@router.get('/navigation-navbars')
def navigation_navbars(request: Request):
    return TEMPLATES.TemplateResponse("pages/navigation-navbars.html", {
        "request": request,
        "config": settings
    })


@router.get('/navigation-nav-tabs')
def navigation_nav_tabs(request: Request):
    return TEMPLATES.TemplateResponse("pages/navigation-nav-tabs.html", {
        "request": request,
        "config": settings
    })


@router.get('/navigation-pagination')
def navigation_pagination(request: Request):
    return TEMPLATES.TemplateResponse("pages/navigation-pagination.html", {
        "request": request,
        "config": settings
    })


@router.get('/input-areas-inputs')
def input_areas_inputs(request: Request):
    return TEMPLATES.TemplateResponse("pages/input-areas-inputs.html", {
        "request": request,
        "config": settings
    })


@router.get('/input-areas-forms')
def input_areas_forms(request: Request):
    return TEMPLATES.TemplateResponse("pages/input-areas-forms.html", {
        "request": request,
        "config": settings
    })


@router.get('/attention-catchers-alerts')
def attention_catchers_alerts(request: Request):
    return TEMPLATES.TemplateResponse("pages/attention-catchers-alerts.html", {
        "request": request,
        "config": settings
    })


@router.get('/attention-catchers-modals')
def attention_catchers_modals(request: Request):
    return TEMPLATES.TemplateResponse("pages/attention-catchers-modals.html", {
        "request": request,
        "config": settings
    })


@router.get('/attention-catchers-tooltips-popovers')
def attention_catchers_tooltips_popovers(request: Request):
    return TEMPLATES.TemplateResponse("pages/attention-catchers-tooltips-popovers.html", {
        "request": request,
        "config": settings
    })


@router.get('/elements-buttons')
def elements_buttons(request: Request):
    return TEMPLATES.TemplateResponse("pages/elements-buttons.html", {
        "request": request,
        "config": settings
    })


@router.get('/elements-avatars')
def elements_avatars(request: Request):
    return TEMPLATES.TemplateResponse("pages/elements-avatars.html", {
        "request": request,
        "config": settings
    })


@router.get('/elements-dropdowns')
def elements_dropdowns(request: Request):
    return TEMPLATES.TemplateResponse("pages/elements-dropdowns.html", {
        "request": request,
        "config": settings
    })


@router.get('/elements-toggles')
def elements_toggles(request: Request):
    return TEMPLATES.TemplateResponse("pages/elements-toggles.html", {
        "request": request,
        "config": settings
    })


@router.get('/elements-breadcrumbs')
def elements_breadcrumbs(request: Request):
    return TEMPLATES.TemplateResponse("pages/elements-breadcrumbs.html", {
        "request": request,
        "config": settings
    })


@router.get('/elements-badges')
def elements_badges(request: Request):
    return TEMPLATES.TemplateResponse("pages/elements-badges.html", {
        "request": request,
        "config": settings
    })


@router.get('/elements-typography')
def elements_typography(request: Request):
    return TEMPLATES.TemplateResponse("pages/elements-typography.html", {
        "request": request,
        "config": settings
    })


@router.get('/elements-progress-bars')
def elements_progress_bars(request: Request):
    return TEMPLATES.TemplateResponse("pages/elements-progress-bars.html", {
        "request": request,
        "config": settings
    })


@router.get('/categories')
def get_all_categories(request: Request, session: Session = Depends(get_db)):
    stores = session.query(StoreModel).all()
    books = session.query(BookModel).all()
    list_category = session.query(CategoryModel).all()
    list_author = session.query(AuthorModel).all()
    return TEMPLATES.TemplateResponse("ecommerce/categories.html", {
        "request": request,
        "stores": stores,
        "books": books,
        "categories": list_category,
        "authors": list_author,
    })


@router.get('/stores')
def get_all_stores(request: Request, session: Session = Depends(get_db)):
    stores = session.query(StoreModel).all()
    books = session.query(BookModel).all()
    list_category = session.query(CategoryModel).all()
    list_author = session.query(AuthorModel).all()
    return TEMPLATES.TemplateResponse("ecommerce/stores.html", {
        "request": request,
        "stores": stores,
        "books": books,
        "categories": list_category,
        "authors": list_author,
    })

@router.get('/authors')
def get_all_authors(request: Request, session: Session = Depends(get_db)):
    stores = session.query(StoreModel).all()
    books = session.query(BookModel).all()
    list_category = session.query(CategoryModel).all()
    list_author = session.query(AuthorModel).all()
    return TEMPLATES.TemplateResponse("ecommerce/authors.html", {
        "request": request,
        "stores": stores,
        "books": books,
        "categories": list_category,
        "authors": list_author,
    })


@router.get('/authors/{id}')
def get_author(id: int, request: Request, session: SessionLocal = Depends(get_db)):
    author = session.query(AuthorModel).get(id)
    books = author.books
    stores = session.query(StoreModel).all()
    list_category = session.query(CategoryModel).all()
    list_author = session.query(AuthorModel).all()
    return TEMPLATES.TemplateResponse("ecommerce/author-detail.html", {
        "request": request,
        "categories": list_category,
        "authors": list_author,
        "books": books,
        "author": author,
        "stores": stores,
    })


@router.get('/categories/{id}')
def get_category(id: int, request: Request, session: SessionLocal = Depends(get_db)):
    category = session.query(CategoryModel).get(id)
    store = session.query(StoreModel).filter(StoreModel.id == id).first()
    list_category = session.query(CategoryModel).all()
    list_author = session.query(AuthorModel).all()
    list_stores = session.query(StoreModel).all()
    return TEMPLATES.TemplateResponse("ecommerce/categories_book.html", {
        "request": request,
        "books": category.list_book,
        "store": store,
        "categories": list_category,
        "authors": list_author,
        "stores": list_stores,
    })
@router.get('/stores/{id}')
def get_store(id: int, request: Request, session: SessionLocal = Depends(get_db)):
    books = session.query(BookModel).filter(BookModel.store_id == id).all()
    store = session.query(StoreModel).filter(StoreModel.id == id).first()
    best_book = books[0]

    if len(books) % 2 == 0 or len(books) % 2 != 0:
        mid = len(books) // 1
        books_part1 = books[0::mid]
        books_part2 = books[mid::]
    else:
        books_part1 = None
        books_part2 = None
    list_category = session.query(CategoryModel).all()
    list_author = session.query(AuthorModel).all()
    list_stores = session.query(StoreModel).all()
    return TEMPLATES.TemplateResponse("pages/stores_book.html", {
        "request": request,
        "books": books,
        "books_part1": books_part1,
        "books_part2": books_part2,
        "store": store,
        "categories": list_category,
        "authors": list_author,
        "stores": list_stores,
        "best_book": best_book
    })


@router.get('/books/{id}')
def get_book(id: int, request: Request, session: SessionLocal = Depends(get_db)):
    book = session.query(BookModel).get(id)
    return TEMPLATES.TemplateResponse("ecommerce/template.html", {
        "request": request,
        "book": book,
        "config": settings
    })


@router.get('/add-to-cart')
def get_help(request: Request, session=Depends(get_db)):
    return TEMPLATES.TemplateResponse("ecommerce/cart.html", {
        "request": request
    })



@router.get('/stores/{id}')
def get_store(id: int, request: Request, session: SessionLocal = Depends(get_db)):
    books = session.query(BookModel).filter(BookModel.store_id == id).all()
    store = session.query(StoreModel).filter(StoreModel.id == id).first()
    best_book = books[0]

    if len(books) % 2 == 0:
        mid = len(books) // 2
        books_part1 = books[0::mid]
        books_part2 = books[mid::]
    else:
        books_part1 = None
        books_part2 = None
    list_category = session.query(CategoryModel).all()
    list_author = session.query(AuthorModel).all()
    list_stores = session.query(StoreModel).all()
    list_book = session.query(BookModel.image).all()
    return TEMPLATES.TemplateResponse("pages/stores_book.html", {
        "request": request,
        "books": books,
        "books_part1": books_part1,
        "books_part2": books_part2,
        "store": store,
        "categories": list_category,
        "authors": list_author,
        "stores": list_stores,
        "best_book": best_book,
        "image": list_book
    })

@router.get("/profiles")
async def get_all_profiles(request: Request, session: Session = Depends(get_db)):
    address = session.query(AddressModel).filter().all()
    user_id = request.session.get('user_id')
    if user_id:
        user = session.query(UserModel).get(user_id)
        if user:
            # addresses = user.list_address
            # order = user.list_order
            return TEMPLATES.TemplateResponse('ecommerce/profile.html', {'request': request, 'user': user, 'address': address})
    return RedirectResponse(url='/')

@router.get("/profiles/{user_id}/edit")
async def edit_profile(request: Request, user_id: int, session: Session = Depends(get_db)):
    user = session.query(UserModel).get(user_id)
    if user:
        return TEMPLATES.TemplateResponse('ecommerce/edit_profile.html', {'request': request, 'user': user})
    return RedirectResponse(url='/')


@router.post("/profiles/{user_id}/edit")
async def update_profile(request: Request, user_id: int, session: Session = Depends(get_db)):
    user = session.query(UserModel).get(user_id)
    if user:
        data = await request.form()
        user.full_name = data['full_name']
        user.email = data['email']
        session.commit()
        return TEMPLATES.TemplateResponse('ecommerce/profile.html', {'request': request, 'user': user})
    return









