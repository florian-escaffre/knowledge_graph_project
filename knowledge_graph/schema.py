from cognee.low_level import DataPoint, Edge


class Technology(DataPoint):
    name: str
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


class Product(DataPoint):
    name: str
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


class Organization(DataPoint):
    name: str
    manufactures: list[Product] | None = None    
    supplier_of: list[Edge["Organization", "Organization"]] = []
    partner_of: list[Edge["Organization", "Organization"]] = []
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


class System(DataPoint):
    name: str
    part_of: list[Product] | None = None
    uses: list[Technology] | None = None
    integrates_with: list[Edge["System", "System"]] = []
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


class Component(DataPoint):
    name: str
    part_of_system: list[System] | None = None
    part_of_component: list[Edge["Component", "Component"]] = []
    uses: list[Technology] | None = None
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


class Project(DataPoint):
    name: str
    develops_product: list[Product] | None = None
    develops_system: list[System] | None = None
    uses: list[Technology] | None = None
    owned_by: list[Organization] | None = None
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


class Role(DataPoint):
    name: str
    member_of: list[Organization] | None = None
    reports_to: list[Edge["Role", "Role"]] = []
    works_on: list[Project] | None = None
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


class EngipediaGraph(DataPoint):
    roles: list[Role] = []
    projects: list[Project] = []
    components: list[Component] = []
    systems: list[System] = []
    organizations: list[Organization] = []
    products: list[Product] = []
    technologies: list[Technology] = []
    metadata: dict = {"index_fields": [], "transparent": True}