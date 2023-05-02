from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, \
    TIMESTAMP, JSON, ForeignKey, func, text, inspect
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM
from .db import engine

Base = declarative_base()
engine = engine

class CategorieUser(Base):
    __tablename__ = "categorie_users"
    
    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False, unique=True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String(225), nullable = False)
    email = Column(String(225), nullable = False, unique = True)
    numero_telephone = Column(String(225), unique = True)
    password = Column(Text, nullable = False)
    birthdate = Column(DateTime)
    sex = Column(String(225))
    address = Column(String(225))
    profile_url = Column(String(225))
    is_active = Column(Boolean, nullable = False, default = True)
    categorie_user_id = Column(Integer, ForeignKey('categorie_users.id'))
    categorie_user = relationship('CategorieUser', )
    email_verified_at = Column(TIMESTAMP, default = None)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False, unique=True)
    permissions = Column(JSON)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key = True, )
    libelle = Column(String(225), nullable = False)
    slug = Column(String(225), nullable = False, unique = True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }



class Dossier(Base):
    __tablename__ = "dossiers"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates = "dossiers")
    numero_dossier = Column(String(225), nullable = False, unique=True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


User.dossiers = relationship("Dossier", order_by = Dossier.id, back_populates = "user")

class Pays(Base):
    __tablename__ = "pays"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False, unique = True)
    code = Column(String(225), nullable = False, unique = True)
    monnaie = Column(String(225))
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

        
class TypeDemande(Base):
    __tablename__ = "type_demandes"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False)
    pays_id = Column(Integer, ForeignKey('pays.id'))
    pays = relationship("Pays", back_populates = "type_demandes")
    tarif = Column(Integer)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    

Pays.type_demandes = relationship('TypeDemande', order_by = TypeDemande.id, back_populates = "pays")


class EtatDemande(Base):
    __tablename__ = "etat_demandes"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False, unique=True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class EtapeTraitement(Base):
    __tablename__ = "etape_traitements"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False, unique=False)
    is_default = Column(Boolean, nullable = False)
    type_demande_id = Column(Integer, ForeignKey('type_demandes.id'))
    type_demande = relationship("TypeDemande", back_populates = "etape_traitements")
    faq = Column(JSON)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


TypeDemande.etape_traitements = relationship("EtapeTraitement", order_by = EtapeTraitement.id,  back_populates = "type_demande")


class EtatEtapeTraitement(Base):
    __tablename__ = "etat_etape_traitements"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False)
    is_default = Column(Boolean, nullable = False)
    chemin_mail = Column(String(225), nullable = True)
    is_mail = Column(Boolean, nullable = True)
    etape_traitement_id = Column(Integer, ForeignKey('etape_traitements.id'))
    etape_traitement = relationship("EtapeTraitement", back_populates = "etat_etape_traitements")
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


EtapeTraitement.etat_etape_traitements = relationship("EtatEtapeTraitement", order_by = EtatEtapeTraitement.id,  back_populates = "etape_traitement")


class TypePaiement(Base):
    __tablename__ = "type_paiements"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False, unique=True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class MoyenPaiement(Base):
    __tablename__ = "moyen_paiements"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False, unique=True)
    is_private = Column(Boolean)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Demande(Base):
    __tablename__ = "demandes"

    id = Column(Integer, primary_key = True)
    dossier_id = Column(Integer, ForeignKey('dossiers.id'))
    dossier = relationship("Dossier", back_populates = "demandes")
    champs_demande = Column(JSON)
    champs_questionnaire = Column(JSON)
    champs_etape_traitements = Column(JSON)
    type_demande_id = Column(Integer, ForeignKey('type_demandes.id'))
    type_demande = relationship("TypeDemande", back_populates = "demandes")
    etape_traitement_id = Column(Integer, ForeignKey('etape_traitements.id'))
    etape_traitement = relationship("EtapeTraitement", back_populates = "demandes")
    pays_id = Column(Integer, ForeignKey('pays.id'))
    pays = relationship("Pays", back_populates = "demandes")
    etat_demande_id = Column(Integer, ForeignKey('etat_demandes.id'))
    etat_demande = relationship("EtatDemande", back_populates = "demandes")
    numero_demande = Column(String(225), unique=True, nullable = False)
    montant_total = Column(Integer, nullable = True)
    montant_paye = Column(Integer, nullable = True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


Dossier.demandes = relationship("Demande", order_by = Demande.id,  back_populates = "dossier")
TypeDemande.demandes = relationship("Demande", order_by = Demande.id,  back_populates = "type_demande")
EtapeTraitement.demandes = relationship("Demande", order_by = Demande.id,  back_populates = "etape_traitement")
Pays.demandes = relationship("Demande", order_by = Demande.id,  back_populates = "pays")
EtatDemande.demandes = relationship("Demande", order_by = Demande.id,  back_populates = "etat_demande")


class StatusEtatTraitement(Base):
    __tablename__ = "status_etat_traitements"

    id = Column(Integer, primary_key = True)
    demande_id = Column(Integer, ForeignKey('demandes.id'))
    demande = relationship("Demande", back_populates = "status_etat_traitements")
    etape_traitement_id = Column(Integer, ForeignKey('etape_traitements.id'))
    etape_traitement = relationship("EtapeTraitement", back_populates = "status_etat_traitements")
    etat_etape_traitement_id = Column(Integer, ForeignKey('etat_etape_traitements.id'))
    etat_etape_traitement = relationship("EtatEtapeTraitement", back_populates = "status_etat_traitements")
    temps_estime = Column(String(225))
    description = Column(Text)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


Demande.status_etat_traitements = relationship("StatusEtatTraitement", order_by = StatusEtatTraitement.id,  back_populates = "demande")
EtapeTraitement.status_etat_traitements = relationship("StatusEtatTraitement", order_by = StatusEtatTraitement.id,  back_populates = "etape_traitement")
EtatEtapeTraitement.status_etat_traitements = relationship("StatusEtatTraitement", order_by = StatusEtatTraitement.id,  back_populates = "etat_etape_traitement")


class CodePromo(Base):
    __tablename__ = "code_promos"

    id = Column(Integer, primary_key = True)
    code = Column(String(255), unique = True)
    pourcentage = Column(Integer)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Paiement(Base):
    __tablename__ = "paiements"

    id = Column(Integer, primary_key = True)
    moyen_paiement_id = Column(Integer, ForeignKey('moyen_paiements.id'), nullable = False)
    moyen_paiement = relationship("MoyenPaiement", back_populates = "paiements") 
    montant = Column(Integer, nullable = False)   
    type_paiement_id = Column(Integer, ForeignKey('type_paiements.id'), nullable = False)
    type_paiement = relationship("TypePaiement", back_populates = "paiements") 
    demande_id = Column(Integer, ForeignKey('demandes.id'), nullable = False)
    demande = relationship("Demande", back_populates = "paiements") 
    status = Column(ENUM('en-cours', 'termine', 'annule'), nullable = False, default = 'en-cours')
    code_promo_id = Column(Integer, ForeignKey('code_promos.id'))
    code_promo = relationship("CodePromo", back_populates = "paiements") 
    recu_paiement_url = Column(String(225))
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


MoyenPaiement.paiements = relationship("Paiement", order_by = Paiement.id,  back_populates = "moyen_paiement")
TypePaiement.paiements = relationship("Paiement", order_by = Paiement.id,  back_populates = "type_paiement")
Demande.paiements = relationship("Paiement", order_by = Paiement.id,  back_populates = "demande")
CodePromo.paiements = relationship("Paiement", order_by = Paiement.id,  back_populates = "code_promo")


class TypeDocument(Base):
    __tablename__ = "type_documents"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False)
    type_demande_id = Column(Integer, ForeignKey('type_demandes.id'), nullable =  False)
    type_demande = relationship("TypeDemande", back_populates = "type_documents")
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


TypeDemande.type_documents = relationship("TypeDocument", order_by = TypeDocument.id,  back_populates = "type_demande")


class EtatDocument(Base):
    __tablename__ = "etat_documents"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False, unique=True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key = True)
    type_document_id = Column(Integer, ForeignKey('type_documents.id'), nullable =  False)
    type_document = relationship("TypeDocument", back_populates = "documents") 
    etat_document_id = Column(Integer, ForeignKey('etat_documents.id'), nullable =  False)
    etat_document = relationship("EtatDocument", back_populates = "documents") 
    demande_id = Column(Integer, ForeignKey('demandes.id'), nullable =  False)
    demande = relationship("Demande", back_populates = "documents") 
    etape_traitement_id = Column(Integer, ForeignKey('etape_traitements.id'))
    etape_traitement = relationship("EtapeTraitement", back_populates = "documents") 
    champs_document = Column(JSON, nullable = False)
    document_url = Column(String(225), nullable =  False)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


TypeDocument.documents = relationship("Document", order_by = Document.id,  back_populates = "type_document")
EtatDocument.documents = relationship("Document", order_by = Document.id,  back_populates = "etat_document")
Demande.documents = relationship("Document", order_by = Document.id,  back_populates = "demande")
EtapeTraitement.documents = relationship("Document", order_by = Document.id,  back_populates = "etape_traitement")


class TypePiece(Base):
    __tablename__ = "type_pieces"

    id = Column(Integer, primary_key = True)
    libelle = Column(String(225), nullable = False)
    type_demande_id = Column(Integer, ForeignKey('type_demandes.id'), nullable =  False)
    type_demande = relationship("TypeDemande", back_populates = "type_pieces")
    is_particulier = Column(Boolean, default=True) 
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


TypeDemande.type_pieces = relationship("TypePiece", order_by = TypePiece.id,  back_populates = "type_demande")


class Piece(Base):
    __tablename__ = "pieces"

    id = Column(Integer, primary_key = True)
    demande_id = Column(Integer, ForeignKey('demandes.id'), nullable = False)
    demande = relationship("Demande", back_populates = "pieces")     
    type_piece_id = Column(Integer, ForeignKey('type_pieces.id'), nullable = False)
    type_piece = relationship("TypePiece", back_populates = "pieces")
    piece_url = Column(String(255))
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


Demande.pieces = relationship("Piece", order_by = Piece.id,  back_populates = "demande")
TypePiece.pieces = relationship("Piece", order_by = Piece.id,  back_populates = "type_piece")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key = True)
    username = Column(String(225), nullable = False)
    email = Column(String(225), nullable = False, unique = True)
    password = Column(Text, nullable = False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates = "admins")     
    pays_id = Column(Integer, ForeignKey('pays.id'))
    pays = relationship("Pays", back_populates = "admins")     
    profile_url = Column(String(255))
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


Role.admins = relationship("Admin", order_by = Role.id,  back_populates = "role")
Pays.admins = relationship("Admin", order_by = Pays.id,  back_populates = "pays")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key =  True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    content = Column(Text, nullable = False)
    type_message = Column(String(225), nullable = False)
    read_at = Column(TIMESTAMP, default = None)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key =  True)
    demande_id = Column(Integer, ForeignKey('demandes.id'))
    demande = relationship("Demande", back_populates = "observations")     
    type_document_id = Column(Integer, ForeignKey('type_documents.id'))
    type_document = relationship("TypeDocument", back_populates = "observations")     
    content = Column(Text, nullable = False)
    document_url = Column(String(225), nullable = False)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


Demande.observations = relationship("Observation", order_by = Demande.id,  back_populates = "demande")
TypeDocument.observations = relationship("Observation", order_by = Demande.id,  back_populates = "type_document")


class Attribution(Base):
    __tablename__ = "attributions"

    id = Column(Integer, primary_key =  True)
    commercial_id = Column(Integer)
    juriste_id = Column(Integer)
    formaliste_id = Column(Integer)
    demande_id = Column(Integer, ForeignKey('demandes.id'))
    demande = relationship("Demande", back_populates = "attributions")     
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


Demande.attributions = relationship("Attribution", order_by = Demande.id,  back_populates = "demande")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key =  True)
    nom_auteur = Column(String(225), nullable = True)
    fonction_auteur = Column(String(225), nullable = True)
    photo_auteur = Column(String(225), nullable = True)
    image_article = Column(String(225), nullable = True)
    titre_article = Column(String(225), nullable = True)
    duree_article = Column(String(225), nullable = True)
    url_article = Column(String(225), nullable = True)
    resume_article = Column(Text, nullable = True)
    is_status = Column(Boolean, nullable = False, default = True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class CategorieArticle(Base):
    __tablename__ = "categorie_articles"

    id = Column(Integer, primary_key =  True)
    libelle = Column(String(225), nullable = True)
    description = Column(String(225), nullable = True)
    is_status = Column(Boolean, nullable = False, default = True)
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class ArticleCategorieArticle(Base):
    __tablename__ = "article_categorie_articles"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    article = relationship("Article", back_populates = "article_categorie_articles")     
    categorie_article_id = Column(Integer, ForeignKey('categorie_articles.id'))
    categorie_article = relationship("CategorieArticle", back_populates = "article_categorie_articles")
    created_at = Column(TIMESTAMP, nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column(TIMESTAMP, default = None)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

Article.article_categorie_articles = relationship("ArticleCategorieArticle", order_by = Article.id,  back_populates = "article")
CategorieArticle.article_categorie_articles = relationship("ArticleCategorieArticle", order_by = CategorieArticle.id,  back_populates = "categorie_article")

Base.metadata.create_all(engine)