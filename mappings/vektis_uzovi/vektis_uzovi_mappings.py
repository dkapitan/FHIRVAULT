from domainmodel.identity_domain import *
from pyelt.mappings.sor_to_dv_mappings import SorToEntityMapping, SorToLinkMapping
from pyelt.mappings.source_to_sor_mappings import SourceToSorMapping
from pyelt.sources.files import CsvFile


__author__ = 'cmesu'

#todo eventueel: bestand van vektis-uzovi moet worden voorbereid. Gaat nu handmatig.
# -van xls met tabladen naar .csv
# -alle returns in text-velden eruit
# -alle ; en | in text velden eruit
# - dubbele laatste mutatie kolom van rol eruit halen

def init_source_to_sor_mappings(path):
    mappings = []

    ###############################
    # UZOVI
    # gangbare rollen: ZV, CV, GA, LA
    ###############################
    source_file = CsvFile(path + '20160419_UZOVI_register_met_relaties.csv', delimiter=';', encoding='LATIN1')
    source_file.set_primary_key(['UZOVI_code', 'Begindatum', 'Relatie_met_UZOVI_code', 'Relatierol', 'Begindatum_relatie'])
    sor_mapping = SourceToSorMapping(source_file, 'uzovi_hstage', auto_map=True)
    mappings.append(sor_mapping)


    return mappings


def init_sor_to_dv_mappings(pipe):
    mappings = []
    mapping = SorToEntityMapping('uzovi_hstage', Zorgverzekeraar, pipe.sor)
    mapping.map_bk(["right('0'||uzovi_code, 4)"])
    mapping.map_field("right('0'||uzovi_code, 4)", Zorgverzekeraar.Uzovi.uzovi_nummer)
    mapping.map_field('naam', Zorgverzekeraar.Default.naam)
    mapping.filter = "einddatum IS NULL"
    mappings.append(mapping)

    mapping = SorToEntityMapping('uzovi_hstage', Zorginkoopcombinatie, pipe.sor)
    mapping.map_bk(['coalesce(inkoopconcern, concern)'])
    mapping.map_field('coalesce(inkoopconcern, concern)', Zorginkoopcombinatie.Default.naam)
    mapping.filter = "coalesce(inkoopconcern, concern) is not null"
    mappings.append(mapping)

    link_mapping = SorToLinkMapping('uzovi_hstage', ZorginkoopcombinatieLinkEntity, pipe.sor)
    link_mapping.map_entity(ZorginkoopcombinatieLinkEntity.Link.verzekeraar)
    link_mapping.map_entity(ZorginkoopcombinatieLinkEntity.Link.inkoopcombinatie)
    mappings.append(link_mapping)

    link_mapping = SorToLinkMapping("uzovi_hstage", ZorgverzekeraarKoepelLinkEntity, pipe.sor)
    link_mapping.map_entity(ZorgverzekeraarKoepelLinkEntity.Link.parent)
    link_mapping.map_entity(ZorgverzekeraarKoepelLinkEntity.Link.child)
    # link_mapping.map_field'uzovi_code', ZorgverzekeraarKoepelLink.parent)
    # link_mapping.map_field('relatie_met_uzovi_code', ZorgverzekeraarKoepelLink.child)
    link_mapping.filter = "relatierol = 'verzekeraar van'"
    mappings.append(link_mapping)

    link_mapping = SorToLinkMapping("uzovi_hstage", ZorgverzekeraarKoepelLinkEntity, pipe.sor)
    link_mapping.map_entity(ZorgverzekeraarKoepelLinkEntity.Link.parent)
    link_mapping.map_entity(ZorgverzekeraarKoepelLinkEntity.Link.child)
    # link_mapping.map_field'uzovi_code', ZorgverzekeraarKoepelLink.parent)
    # link_mapping.map_field('relatie_met_uzovi_code', ZorgverzekeraarKoepelLink.child)
    link_mapping.filter = "relatierol != 'verzekeraar van'"
    mappings.append(link_mapping)

    return mappings


