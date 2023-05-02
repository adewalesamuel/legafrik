import pdfkit
import json
import datetime
from flask import render_template
from os import environ
from . import auth, mail, strings, s3_upload, status_response
import boto3
from botocore.exceptions import NoCredentialsError

from environs import Env

env = Env()
env.read_env()

optionsLandscapeA4 = {
        "orientation": "landscape",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }

optionsPortraitA4 = {
        "orientation": "portrait",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }

optionsA4 = {
        "orientation": "portrait",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }

def test_pdf(options, datas):
    out = render_template("pdf/test.html")
    #pdf = pdfkit.from_string(out, options=options)

    # Chemin vers le fichier PDF à générer
    chemin_fichier_pdf = "public/fichier.pdf"

    #pdfkit.from_file(out, chemin_fichier_pdf, options=options)
    pdf = pdfkit.from_string(out, chemin_fichier_pdf, options=options)

    return 'pdf'

    #try:
    #    a = s3_upload.upload_file_s3(pdf, 'legafrik', 'out.pdf')
    #    return pdf
    #except NoCredentialsError:
    #    return pdf
        # return Response(pdf, mimetype="application/pdf")


  

def gen_recap_demande_pdf(options, datas):

    data = {
            "numero_demande": datas['demande']['numero_demande'],
            "created_at": datas['demande']['created_at'],
            "champs_demande": json.loads(datas['demande']['champs_demande']),
            "champs_questionnaire":json.loads(datas['demande']['champs_questionnaire'])
        }
    
    #champs_demande = json.loads(data.)
    rendered_html = render_template("pdf/gen_recap_demande.html", data=data)
    date_actuelle = datetime.datetime.now()
    date_str = str(date_actuelle)
    date_str = date_str.replace(" ", "")
    date_str = date_str.replace(".", "")
    date_str = date_str.replace(":", "")
    date_str = date_str.replace("-", "")
    pdf = pdfkit.from_string(rendered_html, options=options)
    a = s3_upload.upload_gen_file_s3(pdf, 'legafrik', "gen_recap_demande"+date_str)


    #pdf = pdfkit.from_string(out, options=options)

    # Chemin vers le fichier PDF à générer
    #chemin_fichier_pdf = "public/fichier.pdf"

    #pdfkit.from_file(out, chemin_fichier_pdf, options=options)
    #pdf = pdfkit.from_string(out, chemin_fichier_pdf, options=options)

    return a

    #try:
    #    a = s3_upload.upload_file_s3(pdf, 'legafrik', 'out.pdf')
    #    return pdf
    #except NoCredentialsError:
    #    return pdf
        # return Response(pdf, mimetype="application/pdf")


  

def gen_recap_demande_new_pdf(options, datas):

    champs_questionnaire = json.loads(datas['champs_questionnaire'])


    try:
        addresse = json.loads(champs_questionnaire['addresse'])
    except Exception as err:
        addresse = []

    try:
        gerants = json.loads(champs_questionnaire['gerants'])
    except Exception as err:
        gerants = "Aucun"

    try:
        president = json.loads(champs_questionnaire['president'])
    except Exception as err:
        president = "Aucun"

    try:
        directeur = json.loads(champs_questionnaire['directeur'])
    except Exception as err:
        directeur = "Aucun"

    data = {
            "user": datas['user'],
            "type_demande": datas['type_demande'],
            "pays": datas['pays'],
            "created_at": datas['created_at'],
            "numero_demande": datas['numero_demande'],
            "champs_demande": json.loads(datas['champs_demande']),
            "champs_questionnaire": champs_questionnaire,
            "addresse": addresse,
            "associes": json.loads(champs_questionnaire['associes']),
            "gerants": gerants,
            "president": president,
            "directeur": directeur
        }
    
    #champs_demande = json.loads(data.)
    rendered_html = render_template("pdf/gen_recap_demande.html", data=data)
    date_actuelle = datetime.datetime.now()
    date_str = str(date_actuelle)
    date_str = date_str.replace(" ", "")
    date_str = date_str.replace(".", "")
    date_str = date_str.replace(":", "")
    date_str = date_str.replace("-", "")
    pdf = pdfkit.from_string(rendered_html, options=options)
    data_s3 = s3_upload.upload_gen_file_s3(pdf, 'legafrik', "gen_recap_demande"+date_str+".pdf")

    return data_s3
