
## Next Steps

* Result highlights -- done
* No nested indexing -- done
* Demo data loader -- done
* Front-End Navbar -- done
* Collections / Projects -- done
* Roles / Users+Groups -- done
* Add ownership type relation -- done
* Collection permissions -- done
* Source permissions -- done
* Search authz filters -- done (tbd: entity rendering)
* Entity authz filters
* Entities R/W API
* Ownership type (Company, Asset) -- done
* Implement entity auto-suggest
* Collection grid view
* Layout once-over
* Embeddable entities for other sites
* Image uploading/storage for entities

* Records de-ref, layer
* Records indexing


* http://docs.handsontable.com/0.20.0/tutorial-quick-start.html

## Domain Model

Collection
    CollectionEntity

## Permissions/Authorization Model

Role: User, Network, Groups
    id
    name
    type
    is_admin

Resource: Collection, Source

Permission (Identity, Resource)
    role
    resource_type
    resource_id

Places where authz matters:
    * REST API
    * Entity construction

Places where users matter:
    * Collections (create / access)
    * Statement authorship

Statement:
    * subject
    * predicate
    * object
    * source_id
    * collection
    * author
    * created_at
