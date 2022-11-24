# coding: utf-8
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, String, Table, Date, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import relationship

db = SQLAlchemy()
Base = db.Model
metadata = Base.metadata


class Circonscription(Base):
    __tablename__ = 'circonscription'

    id_circonscription = Column(INTEGER(11), primary_key=True)
    zone_libre = Column(String(50), nullable=False)
    zone = Column(VARCHAR(50), nullable=False)


class Cycle(Base):
    __tablename__ = 'cycle'

    id_cycle = Column(INTEGER(11), primary_key=True)
    lib_cycle = Column(String(50), nullable=False)


class DnmaProfil(Base):
    __tablename__ = 'dnma_profil'

    id_profil = Column(INTEGER(11), primary_key=True)
    lib_profil = Column(String(100), nullable=False)
    lib_court = Column(String(50), nullable=False)


class Enseignement(Base):
    __tablename__ = 'enseignement'

    id_enseignement = Column(INTEGER(11), primary_key=True)
    lib_enseignement = Column(String(200), nullable=False)

class ErreurMarquage(Base):
    __tablename__ = 'erreur_marquage'

    id_erreur = Column(INTEGER(11), primary_key=True)
    date = Column(Date, nullable=False)
    id_site = Column(String(10), nullable=False)
    indicateur = Column(String(25), nullable=False)
    valeur = Column(String(50), nullable=False)
    visites = Column(INTEGER(11), nullable=False)

class Exploitant(Base):
    __tablename__ = 'exploitant'

    id_exploitant = Column(INTEGER(11), primary_key=True)
    lib_exploitant_long = Column(String(50), nullable=False)
    lib_exploitant_court = Column(String(50), nullable=False)
    role = Column(ForeignKey('exploitant_role.role', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    etat = Column(INTEGER(11), nullable=False)

    plateforme = relationship('Plateforme', back_populates='exploitant')
    titulaire_marche = relationship('TitulaireMarche', back_populates='exploitant')
    exploitant_role = relationship('ExploitantRole', back_populates='exploitant')

    @staticmethod
    # method create() create an object and save it in the db
    def create(lib_exploitant_long, lib_exploitant_court, role, etat):
        new_exploitant = Exploitant(lib_exploitant_long=lib_exploitant_long,
                                lib_exploitant_court=lib_exploitant_court, role=role,
                                etat=etat)
        db.session.add(new_exploitant)
        db.session.commit()
        return new_exploitant

class ExploitantRole(Base):
    __tablename__ = 'exploitant_role'

    role = Column(INTEGER(11), primary_key=True)
    libelle_role = Column(String(200), nullable=False)
    
    exploitant = relationship('Exploitant', back_populates='exploitant_role')

class Log(Base):
    __tablename__ = 'log'

    id_log = Column(INTEGER(11), primary_key=True)
    type_log = Column(INTEGER(11), nullable=False)
    id_object = Column(INTEGER(11), nullable=False)
    type_object = Column(INTEGER(11), nullable=False)
    date = Column(Date, nullable=False)
    id_user = Column(INTEGER(11), nullable=False)

class Marche(Base):
    __tablename__ = 'marche'

    id_marche = Column(INTEGER(11), primary_key=True)
    lib_marche = Column(String(200), nullable=False)
    commentaire = Column(String(500), nullable=False)
    date_debut_marche = Column(Date, nullable=False)
    date_fin_marche = Column(Date)
    duree_maximale = Column(INTEGER(11), nullable=False)

    titulaire_marche = relationship('TitulaireMarche', back_populates='marche')

    @staticmethod
    # method create() create an object and save it in the db
    def create(id_marche, lib_marche, commentaire, date_debut_marche, date_fin_marche, duree_maximale):
        new_market = Marche(id_marche=id_marche, 
                                lib_marche=lib_marche,
                                commentaire=commentaire,
                                date_debut_marche=date_debut_marche,
                                date_fin_marche=date_fin_marche,
                                duree_maximale=duree_maximale
                                )
        db.session.add(new_market)
        db.session.commit()
        return new_market

class Ministere(Base):
    __tablename__ = 'ministere'

    id_ministere = Column(INTEGER(11), primary_key=True)
    acronyme_ministere = Column(String(10), nullable=False)
    lib_ministere = Column(String(100), nullable=False)

    uais1 = relationship('Uai', back_populates='ministere')

    @staticmethod
    # method create() create an object and save it in the db
    def create(id_ministere, acronyme_ministere, lib_ministere):
        new_ministere = Ministere(id_ministere=id_ministere,
                                acronyme_ministere=acronyme_ministere,
                                lib_ministere=lib_ministere)
        db.session.add(new_ministere)
        db.session.commit()
        return new_ministere


class Nature(Base):
    __tablename__ = 'nature'

    code_nature = Column(INTEGER(11), primary_key=True)
    type_uai = Column(String(10), nullable=False)
    nature_uai_libelle = Column(String(100), nullable=False)

    cycle = relationship('Cycle', secondary='correspondance_nature_cycle')
    uai = relationship('Uai', back_populates='nature',uselist=False)
    

class Niveau(Base):
    __tablename__ = 'niveau'

    id_niveau = Column(INTEGER(11), primary_key=True)
    lib_niveau = Column(String(20), nullable=False)
    id_enseignement = Column(ForeignKey('enseignement.id_enseignement', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_cycle = Column(ForeignKey('cycle.id_cycle', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    cycle = relationship('Cycle')
    enseignement = relationship('Enseignement')


class ProjetTerritorialUai(Base):
    __tablename__ = 'projet_territorial_uai'

    id_projet_territorial_uai = Column(INTEGER(11), primary_key=True)
    lib_projet_territorial_uai_long = Column(String(50), nullable=False)
    lib_projet_territorial_uai_court = Column(String(50), nullable=False)
    id_type_projet_territorial = Column(ForeignKey('type_projet_territorial.id_type_projet_territorial', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    etat = Column(INTEGER(11), nullable=False)
    
    type_projet_territorial = relationship('TypeProjetTerritorial')
    deploiement_projet_territorial_uai = relationship('DeploiementProjetTerritorialUai', back_populates='projet_territorial_uai')

    titulaire_marche = relationship('TitulaireMarche', back_populates='projet_territorial_uai')

    @staticmethod
    # method create() create an object and save it in the db
    def create(id_projet_territorial_uai, lib_projet_territorial_uai_long, lib_projet_territorial_uai_court, id_type_projet_territorial):
        new_territorial_project = ProjetTerritorialUai(id_projet_territorial_uai=id_projet_territorial_uai, 
                                lib_projet_territorial_uai_long=lib_projet_territorial_uai_long,
                                lib_projet_territorial_uai_court=lib_projet_territorial_uai_court,
                                id_type_projet_territorial=id_type_projet_territorial
                                )
        db.session.add(new_territorial_project)
        db.session.commit()
        return new_territorial_project

class ProjetNational(Base):
    __tablename__ = 'projet_national'

    id_projet_nat = Column(INTEGER(11), primary_key=True)
    lib_projet_nat = Column(String(30), nullable=False)


class Region(Base):
    __tablename__ = 'region'

    code_region = Column(VARCHAR(2), primary_key=True)
    libelle_region = Column(VARCHAR(26), nullable=False)


class RegionAcademique(Base):
    __tablename__ = 'region_academique'

    id_region_academique = Column(INTEGER(11), primary_key=True)
    lib_region_academique = Column(String(500), nullable=False)

class Statut(Base):
    __tablename__ = 'statut'

    id_satut = Column(INTEGER(11), primary_key=True)
    lib_statut = Column(String(200), nullable=False)


class TypeCollectivite(Base):
    __tablename__ = 'type_collectivite'

    id_type_collectivite = Column(INTEGER(11), primary_key=True)
    lib_type_collectivite = Column(String(50), nullable=False)


class TypeProjetTerritorial(Base):
    __tablename__ = 'type_projet_territorial'

    id_type_projet_territorial = Column(INTEGER(11), primary_key=True)
    lib_type_projet_territorial = Column(String(30), nullable=False)

    plateforme = relationship('Plateforme', back_populates='type_projet_territorial')
class Academie(Base):
    __tablename__ = 'academie'

    id_academie = Column(INTEGER(11), primary_key=True)
    lib_academie = Column(String(50), nullable=False)
    nouvel_id_academie = Column(ForeignKey('academie.id_academie', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    id_region_academique = Column(
        ForeignKey('region_academique.id_region_academique', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    region_academique = relationship('RegionAcademique')
    uais = relationship('Uai', back_populates='academie')

    @staticmethod
    # method create() create an object and save it in the db
    def create(lib_academie, nouvel_id_academie, id_region_academique):
        new_academie = Plateforme(lib_academie=lib_academie,
                                nouvel_id_academie=nouvel_id_academie,
                                id_region_academique=id_region_academique)
        db.session.add(new_academie)
        db.session.commit()
        return new_academie


class AliasExploitant(Base):
    __tablename__ = 'alias_exploitant'

    id_alias_exploitant = Column(String(50), primary_key=True)
    id_exploitant = Column(ForeignKey('exploitant.id_exploitant', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_projet_nat = Column(ForeignKey('projet_national.id_projet_nat', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    lib_alias_exploitant = Column(String(30), nullable=False)

    exploitant = relationship('Exploitant')
    projet_national = relationship('ProjetNational')



t_correspondance_nature_cycle = Table(
    'correspondance_nature_cycle', metadata,
    Column('code_nature', ForeignKey('nature.code_nature', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
           nullable=False, index=True),
    Column('id_cycle', ForeignKey('cycle.id_cycle', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
           nullable=False, index=True)
)

class CorrespondanceNatureEnseignement(Base):
    __tablename__ = 'correspondance_nature_enseignement'

    code_nature = Column(INTEGER(11), primary_key=True, index=True)
    id_enseignement = Column(ForeignKey('enseignement.id_enseignement', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    enseignement = relationship('Enseignement')

class Departement(Base):
    __tablename__ = 'departement'

    code_departement = Column(String(3), primary_key=True)
    code_region = Column(ForeignKey('region.code_region', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    libelle_departement = Column(VARCHAR(23), nullable=False)

    region = relationship('Region')


class DnmaQualification(Base):
    __tablename__ = 'dnma_qualification'

    id_qualif = Column(INTEGER(11), primary_key=True)
    id_statut = Column(ForeignKey('statut.id_satut'), nullable=False, index=True)
    site = Column(String(200), nullable=False)
    s2 = Column(String(200), nullable=False)
    date_debut = Column(String(200))
    date_fin = Column(String(200))
    commentaire = Column(String(200))

    statut = relationship('Statut')

class Plateforme(Base):
    __tablename__ = 'plateforme'

    id_plateforme = Column(INTEGER(11), primary_key=True)
    lib_plateforme_long = Column(String(50), nullable=False)
    lib_plateforme_court = Column(String(50), nullable=False)
    id_editeur = Column(ForeignKey('exploitant.id_exploitant', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    etat = Column(INTEGER(11), nullable=False)
    id_type_projet_territorial = Column(ForeignKey('type_projet_territorial.id_type_projet_territorial', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    exploitant = relationship('Exploitant', back_populates='plateforme')
    type_projet_territorial = relationship('TypeProjetTerritorial', back_populates='plateforme')
    deploiement_projet_territorial_uai = relationship('DeploiementProjetTerritorialUai', back_populates='plateforme')
    titulaire_marche = relationship('TitulaireMarche', back_populates='plateforme')

    @staticmethod
    # method create() create an object and save it in the db
    def create(id_plateforme, lib_plateforme_long, lib_plateforme_court, id_editeur, etat, id_type_projet_territorial):
        new_plateform = Plateforme(id_plateforme=id_plateforme, lib_plateforme_long=lib_plateforme_long,
                                lib_plateforme_court=lib_plateforme_court,
                                id_editeur=id_editeur, etat=etat,
                                id_type_projet_territorial = id_type_projet_territorial)
        db.session.add(new_plateform)
        db.session.commit()
        return new_plateform


class AliasPlateforme(Base):
    __tablename__ = 'alias_plateforme'

    id_alias_plateforme = Column(String(50), primary_key=True)
    id_plateforme = Column(ForeignKey('plateforme.id_plateforme', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_projet_nat = Column(ForeignKey('projet_national.id_projet_nat'), nullable=False, index=True)
    lib_alias_plateforme = Column(String(30), nullable=False)

    plateforme = relationship('Plateforme')
    projet_national = relationship('ProjetNational')


class AliasProjetTerritorialUai(Base):
    __tablename__ = 'alias_projet_territorial_uai'

    id_alias_projet_territorial_uai = Column(String(50), primary_key=True)
    id_projet_territorial_uai = Column(ForeignKey('projet_territorial_uai.id_projet_territorial_uai', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_projet_nat = Column(ForeignKey('projet_national.id_projet_nat', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    lib_alias_projet_territorial_uai = Column(String(30), nullable=False)

    projet_national = relationship('ProjetNational')
    projet_territorial_uai = relationship('ProjetTerritorialUai')



class Commune(Base):
    __tablename__ = 'commune'

    code_commune = Column(String(5), primary_key=True)
    code_region = Column(ForeignKey('region.code_region', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    code_departement = Column(ForeignKey('departement.code_departement', ondelete='CASCADE', onupdate='CASCADE'),
                              index=True)
    lib_commune = Column(String(100))
    code_postal = Column(String(10))

    departement = relationship('Departement')
    region = relationship('Region')


class TitulaireMarche(Base):
    __tablename__ = 'titulaire_marche'
    id_titulaire_marche = Column(INTEGER(11), primary_key=True)
    id_plateforme = Column(ForeignKey('plateforme.id_plateforme', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_projet_territorial_uai= Column(ForeignKey('projet_territorial_uai.id_projet_territorial_uai', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_exploitant = Column(ForeignKey('exploitant.id_exploitant', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_marche = Column(ForeignKey('marche.id_marche', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    plateforme = relationship('Plateforme', back_populates='titulaire_marche')
    marche = relationship('Marche', back_populates='titulaire_marche')
    exploitant = relationship('Exploitant', back_populates='titulaire_marche')
    projet_territorial_uai = relationship('ProjetTerritorialUai', back_populates='titulaire_marche')

    @staticmethod
    # method create() create an object and save it in the db
    def create(id_titulaire_marche, id_plateforme, id_projet_territorial_uai, id_exploitant, id_marche):
        new_official_market = TitulaireMarche(id_titulaire_marche=id_titulaire_marche, 
                                id_plateforme=id_plateforme,
                                id_projet_territorial_uai=id_projet_territorial_uai,
                                id_exploitant=id_exploitant,
                                id_marche=id_marche
                                )
        db.session.add(new_official_market)
        db.session.commit()
        return new_official_market

class Uai(Base):
    __tablename__ = 'uai'

    uai = Column(String(11), primary_key=True)
    collectivite = Column(String(200))
    id_type_collectivite = Column(ForeignKey('type_collectivite.id_type_collectivite', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    patronyme = Column(String(200))
    code_nature = Column(ForeignKey('nature.code_nature', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    code_academie = Column(ForeignKey('academie.id_academie', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                           index=True)
    code_commune = Column(ForeignKey('commune.code_commune', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    etat_etablissement = Column(String(15), nullable=False)
    id_ministere = Column(ForeignKey('ministere.id_ministere', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    id_circonscription = Column(
        ForeignKey('circonscription.id_circonscription', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    boite_postale = Column(String(20))
    secteur = Column(String(2))
    zone_cite_scolaire = Column(String(20))
    sigle_uai = Column(String(100))

    academie = relationship('Academie', back_populates='uais')
    commune = relationship('Commune')
    nature = relationship('Nature', back_populates='uai',uselist=False)
    circonscription = relationship('Circonscription')
    ministere = relationship('Ministere', back_populates='uais1')
    type_collectivite = relationship('TypeCollectivite')
    deploiement_projet_territorial_uai = relationship('DeploiementProjetTerritorialUai', back_populates='uai1')
    effectif = relationship('Effectif', back_populates='uai2')

class DeploiementProjetTerritorialUai(Base):
    __tablename__ = 'deploiement_projet_territorial_uai'

    id_deploiement_projet_territorial_uai = Column(INTEGER(11), primary_key=True)
    uai = Column(ForeignKey('uai.uai'), nullable=False, index=True)
    id_projet_territorial_uai = Column(ForeignKey('projet_territorial_uai.id_projet_territorial_uai', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    id_plateforme = Column(ForeignKey('plateforme.id_plateforme'), index=True)
    date_debut = Column(String(20))
    date_fin = Column(String(20))
    commentaire = Column(String(200))

    plateforme = relationship('Plateforme', back_populates='deploiement_projet_territorial_uai')
    projet_territorial_uai = relationship('ProjetTerritorialUai', back_populates='deploiement_projet_territorial_uai')
    uai1 = relationship('Uai', back_populates='deploiement_projet_territorial_uai',uselist=False)


class DeploiementProjetNational(Base):
    __tablename__ = 'deploiement_projet_national'

    id_deploiement_projet_national = Column(INTEGER(11), primary_key=True)
    id_projet_nat = Column(ForeignKey('projet_national.id_projet_nat', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_deploiement_projet_territorial_uai = Column(ForeignKey('deploiement_projet_territorial_uai.id_deploiement_projet_territorial_uai', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    date_debut = Column(String(20), nullable=False)
    date_fin = Column(String(20), nullable=False)
    commentaire = Column(String(200), nullable=False)

    deploiement_projet_territorial_uai = relationship('DeploiementProjetTerritorialUai')
    projet_national = relationship('ProjetNational')

class Effectif(Base):
    __tablename__ = 'effectif'

    id_effectif = Column(INTEGER(11), primary_key=True)
    periode = Column(String(10), nullable=False)
    id_profil = Column(ForeignKey('dnma_profil.id_profil', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    effectif = Column(INTEGER(11), nullable=False)
    uai = Column(ForeignKey('uai.uai', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id_niveau = Column(ForeignKey('niveau.id_niveau', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    source = Column(String(20))

    niveau = relationship('Niveau')
    dnma_profil = relationship('DnmaProfil')
    uai2 = relationship('Uai', back_populates="effectif")



class ConfigAti(Base):
    __tablename__ = 'config_ati'

    id_config_ati = Column(INTEGER(11), primary_key=True)
    site = Column(String(11), nullable=False)
    id_deploiement_projet_territorial_uai = Column(INTEGER(11), nullable=False, index=True)
    commentaire = Column(String(600))
    etat = Column(String(20), nullable=False)
    marquage_cite_scolaire = Column(String(20))

