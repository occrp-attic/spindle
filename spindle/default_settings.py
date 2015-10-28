DEBUG = True
ASSETS_DEBUG = True
APP_NAME = 'OCCRP Search'

ELASTICSEARCH_HOST = '127.0.0.1:9200'
ELASTICSEARCH_INDEX = 'graph'

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/loom'

SCHEMAS = {
    'legal_person': 'https://schema.occrp.org/generic/legal_person.json#',
    'organization': 'https://schema.occrp.org/generic/organization.json#',
    'person': 'https://schema.occrp.org/generic/person.json#',
    'company': 'https://schema.occrp.org/generic/company.json#',
    'land': 'https://schema.occrp.org/generic/land.json#',
    'building': 'https://schema.occrp.org/generic/building.json#',
    'asset': 'https://schema.occrp.org/generic/asset.json#'
}
