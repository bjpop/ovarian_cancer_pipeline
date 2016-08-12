'''
Build the pipeline workflow by plumbing the stages together.
'''

from ruffus import Pipeline, suffix, formatter, add_inputs, output_from
from stages import PipelineStages 

def make_pipeline(state):
    '''Build the pipeline by constructing stages and connecting them together'''
    # Build an empty pipeline
    pipeline = Pipeline(name='ovarian_cancer_pipeline')
    # Get a list of paths to all the FASTQ files
    fastq_files = state.config.get_option('fastqs')
    human_reference_genome_file = state.config.get_option('human_reference_genome')
    # Stages are dependent on the state
    stages = PipelineStages(state)

    # The original FASTQ files
    # This is a dummy stage. It is useful because it makes a node in the
    # pipeline graph, and gives the pipeline an obvious starting point.
    pipeline.originate(
        task_func=stages.original_fastqs,
        name='original_fastqs',
        output=fastq_files)

    # The human reference genome in FASTA format
    pipeline.originate(
        task_func=stages.human_reference_genome,
        name='human_reference_genome',
        output=human_reference_genome_file)

    # Index the human reference genome with BWA, needed before we can map reads
    pipeline.transform(
        task_func=stages.index_ref_bwa,
        name='index_ref_bwa',
        input=output_from('human_reference_genome'),
        filter=suffix('.fa'),
        output=['.fa.amb', '.fa.ann', '.fa.pac', '.fa.sa', '.fa.bwt'])

    # Align paired end reads in FASTQ to the reference producing a BAM file
    (pipeline.transform(
        task_func=stages.align_bwa,
        name='align_bwa',
        input=output_from('original_fastqs'),
        # Match the R1 (read 1) FASTQ file and grab the path and sample name. 
        # This will be the first input to the stage.
        # We assume the sample name may consist of only alphanumeric
        # characters.
        filter=formatter('.+/(?P<sample>[_a-zA-Z0-9]+)_R1.fastq.gz'),
        # Add one more inputs to the stage:
        #    1. The corresponding R2 FASTQ file
        add_inputs=add_inputs('{path[0]}/{sample[0]}_R2.fastq.gz'),
        # Add an "extra" argument to the state (beyond the inputs and outputs)
        # which is the sample name. This is needed within the stage for finding out
        # sample specific configuration options
        extras=['{sample[0]}'],
        # The output file name is the sample name with a .bam extension.
        output='{path[0]}/{sample[0]}.bam')
        .follows('index_ref_bwa'))


    return pipeline
