from domainmodel_fhir import identity_domain
from domainmodel_fhir.test_config import test_configs
from pyelt.pipeline import Pipeline

pipeline = Pipeline(test_configs)
pipe = pipeline.get_or_create_pipe('test2_system')
pipe.register_domain(identity_domain)
pipeline.run()
