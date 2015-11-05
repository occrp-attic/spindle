
## Next Steps

* Result highlights -- done
* No nested indexing -- done
* Demo data loader -- done
* Front-End Navbar -- done
* Collections / Projects -- done
* Roles / Users+Groups -- done
* Add ownership type relation -- done
* Collection permissions
* Source permissions
* Entities R/W API
* Ownership type (Company, Asset)
* Implement entity auto-suggest
* Collection grid view
* Layout once-over
* Embeddable entities for other sites
* Image uploading/storage for entities

* Records de-ref, layer
* Records indexing

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
