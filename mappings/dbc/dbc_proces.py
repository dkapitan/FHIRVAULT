from domainmodel import valueset_domain
from mappings.dbc.dbc_mappings import init_source_to_sor_mappings, init_sor_to_valset_mappings
from pyelt.pipeline import Pipeline

__author__ = 'hvreenen'


def define_dbc_pipe(pipeline, dbc_config):
    pipe = pipeline.get_or_create_pipe('sor_dbc', dbc_config)
    pipeline.register_valset_domain(valueset_domain, 'valset')

    source_to_sor_mappings = init_source_to_sor_mappings(pipe)
    pipe.mappings.extend(source_to_sor_mappings)

    sor_to_valset_mappings = init_sor_to_valset_mappings(pipe)
    pipe.mappings.extend(sor_to_valset_mappings)
    #
    # sor_to_dv_mappings = init_sor_to_dv_mappings(pipe)
    # pipe.mappings.extend(sor_to_dv_mappings)


def dbc_main(*args):
    from pipelines.general_clinical_configs import general_config, dbc_config
    pipeline = Pipeline(general_config)

    define_dbc_pipe(pipeline, dbc_config)

    pipeline.run()


if __name__ == '__main__':
    dbc_main()

# for filename, file in pipe.source_layer.files.items():
#     for row in file.rows:
#         print(row)
