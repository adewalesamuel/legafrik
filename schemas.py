from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields, validate, validates_schema,\
    ValidationError
from . import models

class CategorieUserSchema(SQLAlchemySchema):
    class Meta:
        model = models.CategorieUser
        load_instance = True
    
    id = auto_field()
    libelle = auto_field()


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = models.User
        load_instance = True
    
    username = auto_field()
    email = auto_field()
    numero_telephone = auto_field()
    password = auto_field()
    birthdate = auto_field()
    sex = auto_field()
    address = auto_field()
    profile_url = auto_field()
    categorie_user_id = auto_field()


class AdminSchema(SQLAlchemySchema):
    class Meta:
        model = models.Admin
        load_instance = True
    
    username = auto_field()
    password = auto_field()
    email = auto_field()
    profile_url = auto_field()
    role_id = auto_field()
    pays_id = auto_field()


class LoginSchema(Schema):
    email = fields.Str(required = True)
    password = fields.Str(required = True)


class UpdateUserSchema(Schema):
    username = fields.Str(required = True)
    email = fields.Email(required = True)
    numero_telephone = fields.Str(validate=validate.Length(min=10), 
                                allow_none = True)
    birthdate = fields.Date(allow_none = True)
    sex = fields.Str(allow_none = True)
    address = fields.Str(allow_none = True)
    profile_url = fields.Str(allow_none = True)


class UpdateAdminSchema(Schema):
    username = fields.Str(required = True)
    email = fields.Email(required = True)
    profile_url = fields.Str(allow_none = True)
    role_id = fields.Integer(allow_none = True)
    pays_id = fields.Integer(allow_none = True)


class UpdatePasswordSchema(Schema):
    password = fields.Str(required = True)
    password_confirmation = fields.Str(required = True)
    
    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["password"] != data["password_confirmation"]:
            raise ValidationError("password must be equal to password_confirmation")

class InitPasswordSchema(Schema):
    password = fields.Str(required = True)
    confirmPassword = fields.Str(required = True)
    token = fields.Str(required = True)
    
    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["password"] != data["confirmPassword"]:
            raise ValidationError("le mot de passe doit être égal au mot de passe de confirmation")


class RoleSchema(SQLAlchemySchema):
    class Meta:
        model = models.Role
        load_instance = True
    
    libelle = auto_field()
    permissions = auto_field()


class PermissionSchema(SQLAlchemySchema):
    class Meta:
        model = models.Permission
        load_instance = True
    
    libelle = auto_field()


class DossierSchema(SQLAlchemySchema):
    class Meta:
        model = models.Dossier
        load_instance = True
    
    user_id = auto_field()
    numero_dossier = auto_field()


class TypeDemandeSchema(SQLAlchemySchema):
    class Meta:
        model = models.TypeDemande
        load_instance = True
    
    libelle = auto_field()
    tarif = auto_field()
    pays_id = auto_field()


class PaysSchema(SQLAlchemySchema):
    class Meta:
        model = models.Pays
        load_instance = True
    
    libelle = auto_field()
    code = auto_field()
    monnaie = auto_field()


class EtatDemandeSchema(SQLAlchemySchema):
    class Meta:
        model = models.EtatDemande
        load_instance = True
    
    libelle = auto_field()


class EtapeTraitementSchema(SQLAlchemySchema):
    class Meta:
        model = models.EtapeTraitement
        load_instance = True
    
    libelle = auto_field()
    type_demande_id = auto_field()
    is_default =  auto_field()
    faq =  auto_field()


class EtatEtapeTraitementSchema(SQLAlchemySchema):
    class Meta:
        model = models.EtatEtapeTraitement
        load_instance = True
    
    libelle = auto_field()
    etape_traitement_id = auto_field()
    is_default =  auto_field()
    #chemin_mail = fields.Str(allow_none = True)
    #is_mail = fields.Str(allow_none = True)


class StatusEtatTraitementSchema(SQLAlchemySchema):
    class Meta:
        model = models.StatusEtatTraitement
        load_instance = True
    
    demande_id = auto_field()
    etape_traitement_id = auto_field()
    etat_etape_traitement_id = auto_field()
    temps_estime = auto_field()
    description = auto_field()


class TypePaiementSchema(SQLAlchemySchema):
    class Meta:
        model = models.TypePaiement
        load_instance = True
    
    libelle = auto_field()


class MoyenPaiementSchema(SQLAlchemySchema):
    class Meta:
        model = models.MoyenPaiement
        load_instance = True
    
    libelle = auto_field()
    is_private = fields.Boolean(required = False, allow_none = True)


class DemandeSchema(SQLAlchemySchema):
    class Meta:
        model = models.Demande
        load_instance = True
    
    dossier_id = auto_field() 
    champs_demande = auto_field()
    type_demande_id = auto_field()
    etape_traitement_id = fields.Integer(required = False, allow_none = True)
    pays_id = auto_field()
    etat_demande_id = fields.Integer(required = False, allow_none = True)
    numero_demande = fields.Str(required = False, allow_none = True)
    montant_total = fields.Integer(required = False, allow_none = True)
    montant_paye = fields.Integer(required = False, allow_none = True)


class ChampsQuestionnaireSchema(SQLAlchemySchema):
    class Meta:
        model = models.Demande
        load_instance = True
    
    champs_questionnaire = auto_field()

class ChampsDemandeCapitalSocialSchema(Schema):    
    capital_social = fields.Str(required = True, allow_none = False)


class ChampsEtapeTraitementSchema(SQLAlchemySchema):
    class Meta:
        model = models.Demande
        load_instance = True

    champs_etape_traitements = auto_field()


class UpdateDemandeEtapeTraitementSchema(SQLAlchemySchema):
    class Meta:
        model = models.Demande
        load_instance = True

    etape_traitement_id = auto_field()


class CodePromoSchema(SQLAlchemySchema):
    class Meta:
        model = models.CodePromo
        load_instance = True
    
    pourcentage = auto_field()
    code = auto_field()


class PaiementSchema(SQLAlchemySchema):
    class Meta:
        model = models.Paiement
        load_instance = True
    
    moyen_paiement_id = auto_field()
    type_paiement_id = auto_field()
    demande_id = auto_field()
    code_promo_id = auto_field()
    montant = fields.Integer(required = False, allow_none = True)
    payment_data = fields.Str(required = False, allow_none = True)


class PaiementLeadSchema(SQLAlchemySchema):
    class Meta:
        model = models.Paiement
        load_instance = True
    
    moyen_paiement_id = auto_field()
    type_paiement_id = auto_field()
    code_promo_id = auto_field()
    montant = fields.Integer(required = False, allow_none = True)
    payment_data = fields.Str(required = False, allow_none = True)


class TypeDocumentSchema(SQLAlchemySchema):
    class Meta:
        model = models.TypeDocument
        load_instance = True
    
    libelle = auto_field()
    type_demande_id = auto_field()


class EtatDocumentSchema(SQLAlchemySchema):
    class Meta:
        model = models.EtatDocument
        load_instance = True
    
    libelle = auto_field()


class DocumentSchema(SQLAlchemySchema):
    class Meta:
        model = models.Document
        load_instance = True
    
    type_document_id = auto_field()
    etat_document_id = auto_field()
    demande_id = auto_field()
    champs_document = auto_field()
    document_url = auto_field()
    etape_traitement_id = auto_field()


class TypePieceSchema(SQLAlchemySchema):
    class Meta:
        model = models.TypePiece
        load_instance = True
    
    libelle = auto_field()
    type_demande_id = auto_field()
    is_particulier = fields.Boolean(required = False, allow_none = True)


class PieceSchema(SQLAlchemySchema):
    class Meta:
        model = models.Piece
        load_instance = True
    
    demande_id = auto_field()
    type_piece_id =  auto_field()
    piece_url =  auto_field()


class MessageSchema(SQLAlchemySchema):
    class Meta:
        model = models.Message
        load_instance = True

    sender_id = fields.Integer(required = False, allow_none = True)
    receiver_id = auto_field()
    content = auto_field()
    type_message = auto_field()


class ObservationSchema(SQLAlchemySchema):
    class Meta:
        model = models.Observation
        load_instance = True
    
    demande_id = auto_field()
    type_document_id = auto_field()
    content = auto_field()
    document_url = auto_field()


class AttributionSchema(SQLAlchemySchema):
    class Meta:
        model = models.Attribution
        load_instance = True
    
    commercial_id = auto_field()
    juriste_id = auto_field()
    formaliste_id = auto_field()
    demande_id = auto_field()


class ArticleSchema(SQLAlchemySchema):
    class Meta:
        model = models.Article
        load_instance = True
    
    nom_auteur = auto_field()
    fonction_auteur = fields.Str(required = False, allow_none = True)
    photo_auteur = fields.Str(required = False, allow_none = True)
    image_article = auto_field()
    titre_article = auto_field()
    duree_article = auto_field()
    resume_article = auto_field()
    is_status = auto_field()
    url_article = auto_field()
    categorie_article_id = fields.Integer(required = False, allow_none = True)

class CategorieArticleSchema(SQLAlchemySchema):
    class Meta:
        model = models.CategorieArticle
        load_instance = True
    
    libelle = auto_field()
    description = auto_field()

class ArticleCategorieArticleSchema(SQLAlchemySchema):
    class Meta:
        model = models.ArticleCategorieArticle
        load_instance = True
    
    
    nom_auteur = fields.Str(required = False, allow_none = True)
    fonction_auteur = fields.Str(required = False, allow_none = True)
    photo_auteur = fields.Str(required = False, allow_none = True)
    image_article = fields.Str(required = False, allow_none = True)
    titre_article = fields.Str(required = False, allow_none = True)
    duree_article = fields.Str(required = False, allow_none = True)
    resume_article = fields.Str(required = False, allow_none = True)
    is_status = fields.Boolean(required = False, allow_none = True)
    url_article = fields.Str(required = False, allow_none = True)
    categorie_article_id = fields.Integer(required = True)