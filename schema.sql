CREATE TABLE categorie_users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:19,882 INFO sqlalchemy.engine.Engine [no key 0.00023s] {}
-- 2023-02-03 14:56:20,178 INFO sqlalchemy.engine.Engine 
CREATE TABLE roles (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	permissions JSON, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:20,179 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
-- 2023-02-03 14:56:20,476 INFO sqlalchemy.engine.Engine 
CREATE TABLE permissions (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	slug VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (slug)
)


-- 2023-02-03 14:56:20,476 INFO sqlalchemy.engine.Engine [no key 0.00035s] {}
-- 2023-02-03 14:56:20,739 INFO sqlalchemy.engine.Engine 
CREATE TABLE type_demandes (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	tarif INTEGER, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:20,739 INFO sqlalchemy.engine.Engine [no key 0.00023s] {}
-- 2023-02-03 14:56:20,972 INFO sqlalchemy.engine.Engine 
CREATE TABLE pays (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	code VARCHAR(225) NOT NULL, 
	monnaie VARCHAR(225), 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle), 
	UNIQUE (code)
)


-- 2023-02-03 14:56:20,973 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
-- 2023-02-03 14:56:21,141 INFO sqlalchemy.engine.Engine 
CREATE TABLE etat_demandes (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:21,141 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
-- 2023-02-03 14:56:21,315 INFO sqlalchemy.engine.Engine 
CREATE TABLE type_paiements (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:21,315 INFO sqlalchemy.engine.Engine [no key 0.00017s] {}
-- 2023-02-03 14:56:21,469 INFO sqlalchemy.engine.Engine 
CREATE TABLE moyen_paiements (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:21,469 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
-- 2023-02-03 14:56:21,621 INFO sqlalchemy.engine.Engine 
CREATE TABLE code_promos (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	code VARCHAR(255), 
	pourcentage INTEGER, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (code)
)


-- 2023-02-03 14:56:21,621 INFO sqlalchemy.engine.Engine [no key 0.00017s] {}
-- 2023-02-03 14:56:21,767 INFO sqlalchemy.engine.Engine 
CREATE TABLE type_documents (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:21,768 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
-- 2023-02-03 14:56:21,923 INFO sqlalchemy.engine.Engine 
CREATE TABLE etat_documents (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:21,923 INFO sqlalchemy.engine.Engine [no key 0.00017s] {}
-- 2023-02-03 14:56:22,067 INFO sqlalchemy.engine.Engine 
CREATE TABLE type_pieces (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle)
)


-- 2023-02-03 14:56:22,067 INFO sqlalchemy.engine.Engine [no key 0.00017s] {}
-- 2023-02-03 14:56:22,240 INFO sqlalchemy.engine.Engine 
CREATE TABLE messages (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	sender_id INTEGER, 
	receiver_id INTEGER, 
	content TEXT NOT NULL, 
	type_message VARCHAR(225) NOT NULL, 
	read_at TIMESTAMP NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id)
)


-- 2023-02-03 14:56:22,240 INFO sqlalchemy.engine.Engine [no key 0.00027s] {}
-- 2023-02-03 14:56:22,386 INFO sqlalchemy.engine.Engine 
CREATE TABLE users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(225) NOT NULL, 
	email VARCHAR(225) NOT NULL, 
	numero_telephone VARCHAR(225), 
	password TEXT NOT NULL, 
	birthdate DATETIME, 
	sex VARCHAR(225), 
	address VARCHAR(225), 
	profile_url VARCHAR(225), 
	is_active BOOL NOT NULL, 
	categorie_user_id INTEGER, 
	email_verified_at TIMESTAMP NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (numero_telephone), 
	FOREIGN KEY(categorie_user_id) REFERENCES categorie_users (id)
)


-- 2023-02-03 14:56:22,386 INFO sqlalchemy.engine.Engine [no key 0.00019s] {}
-- 2023-02-03 14:56:22,530 INFO sqlalchemy.engine.Engine 
CREATE TABLE etape_traitements (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	is_default BOOL NOT NULL, 
	type_demande_id INTEGER, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (libelle), 
	FOREIGN KEY(type_demande_id) REFERENCES type_demandes (id)
)


-- 2023-02-03 14:56:22,530 INFO sqlalchemy.engine.Engine [no key 0.00024s] {}
-- 2023-02-03 14:56:22,678 INFO sqlalchemy.engine.Engine 
CREATE TABLE admins (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(225) NOT NULL, 
	email VARCHAR(225) NOT NULL, 
	password TEXT NOT NULL, 
	role_id INTEGER, 
	profile_url VARCHAR(255), 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
)


-- 2023-02-03 14:56:22,678 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
-- 2023-02-03 14:56:22,797 INFO sqlalchemy.engine.Engine 
CREATE TABLE dossiers (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER, 
	numero_dossier VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	UNIQUE (numero_dossier)
)


-- 2023-02-03 14:56:22,797 INFO sqlalchemy.engine.Engine [no key 0.00029s] {}
-- 2023-02-03 14:56:22,915 INFO sqlalchemy.engine.Engine 
CREATE TABLE etat_etape_traitements (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	libelle VARCHAR(225) NOT NULL, 
	is_default BOOL NOT NULL, 
	chemin_mail VARCHAR(225) NULL, 
	is_mail BOOL NULL, 
	etape_traitement_id INTEGER, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(etape_traitement_id) REFERENCES etape_traitements (id)
)


-- 2023-02-03 14:56:22,915 INFO sqlalchemy.engine.Engine [no key 0.00019s] {}
-- 2023-02-03 14:56:23,083 INFO sqlalchemy.engine.Engine 
CREATE TABLE pieces (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	type_piece_id INTEGER NOT NULL, 
	piece_url VARCHAR(255), 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(type_piece_id) REFERENCES type_pieces (id)
)


-- 2023-02-03 14:56:23,083 INFO sqlalchemy.engine.Engine [no key 0.00021s] {}
-- 2023-02-03 14:56:23,223 INFO sqlalchemy.engine.Engine 
CREATE TABLE status_etat_traitements (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	etape_traitement_id INTEGER, 
	etat_etape_traitement_id INTEGER, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(etape_traitement_id) REFERENCES etape_traitements (id), 
	FOREIGN KEY(etat_etape_traitement_id) REFERENCES etat_etape_traitements (id)
)


-- 2023-02-03 14:56:23,223 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
-- 2023-02-03 14:56:23,371 INFO sqlalchemy.engine.Engine 
CREATE TABLE demandes (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	dossier_id INTEGER, 
	champs_demande JSON, 
	type_demande_id INTEGER, 
	etape_traitement_id INTEGER, 
	pays_id INTEGER, 
	etat_demande_id INTEGER, 
	numero_demande VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(dossier_id) REFERENCES dossiers (id), 
	FOREIGN KEY(type_demande_id) REFERENCES type_demandes (id), 
	FOREIGN KEY(etape_traitement_id) REFERENCES etape_traitements (id), 
	FOREIGN KEY(pays_id) REFERENCES pays (id), 
	FOREIGN KEY(etat_demande_id) REFERENCES etat_demandes (id), 
	UNIQUE (numero_demande)
)


-- 2023-02-03 14:56:23,371 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
-- 2023-02-03 14:56:23,529 INFO sqlalchemy.engine.Engine 
CREATE TABLE paiements (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	moyen_paiement_id INTEGER NOT NULL, 
	montant INTEGER NOT NULL, 
	type_paiement_id INTEGER NOT NULL, 
	demande_id INTEGER NOT NULL, 
	status ENUM('en-cours','termine','annule') NOT NULL, 
	code_promo_id INTEGER, 
	recu_paiement_url VARCHAR(225), 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(moyen_paiement_id) REFERENCES moyen_paiements (id), 
	FOREIGN KEY(type_paiement_id) REFERENCES type_paiements (id), 
	FOREIGN KEY(demande_id) REFERENCES demandes (id), 
	FOREIGN KEY(code_promo_id) REFERENCES code_promos (id)
)


-- 2023-02-03 14:56:23,529 INFO sqlalchemy.engine.Engine [no key 0.00027s] {}
-- 2023-02-03 14:56:23,749 INFO sqlalchemy.engine.Engine 
CREATE TABLE documents (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	type_document_id INTEGER NOT NULL, 
	etat_document_id INTEGER NOT NULL, 
	demande_id INTEGER NOT NULL, 
	champs_document JSON NOT NULL, 
	document_url VARCHAR(225) NOT NULL, 
	created_at TIMESTAMP NOT NULL DEFAULT now(), 
	updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
	deleted_at TIMESTAMP NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(type_document_id) REFERENCES type_documents (id), 
	FOREIGN KEY(etat_document_id) REFERENCES etat_documents (id), 
	FOREIGN KEY(demande_id) REFERENCES demandes (id)
)

CREATE TABLE articles (
	id INTEGER NOT NULL AUTO_INCREMENT, 
    nom_auteur VARCHAR(225),
    fonction_auteur VARCHAR(225),
    photo_auteur VARCHAR(225),
    image_article VARCHAR(225),
    titre_article VARCHAR(225),
    url_article VARCHAR(225),
    duree_article VARCHAR(225),
    resume_article TEXT,
    is_status BOOLEAN NOT NULL DEFAULT TRUE,
	PRIMARY KEY (id), 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE categorie_articles (
	id INTEGER NOT NULL AUTO_INCREMENT, 
    libelle VARCHAR(225),
    description VARCHAR(225),
    is_status BOOLEAN NOT NULL DEFAULT TRUE,
	PRIMARY KEY (id), 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE article_categorie_articles (
	id INTEGER NOT NULL AUTO_INCREMENT, 
    article_id INT NOT NULL,
    categorie_article_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,
	PRIMARY KEY (id), 
    FOREIGN KEY (article_id) REFERENCES articles(id),
    FOREIGN KEY (categorie_article_id) REFERENCES categorie_articles(id)
);

-- 2023-02-03 14:56:23,749 INFO sqlalchemy.engine.Engine [no key 0.00019s] {}
-- 2023-02-03 14:56:23,925 INFO sqlalchemy.engine.Engine COMMIT