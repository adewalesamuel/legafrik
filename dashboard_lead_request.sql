SELECT type_demandes.id, type_demandes.libelle, 
(SELECT COUNT(demandes.id) FROM demandes WHERE type_demande_id=type_demandes.id) 
FROM type_demandes

