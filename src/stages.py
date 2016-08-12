'''
Individual stages of the pipeline implemented as functions from
input files to output files.

The run_stage function knows everything about submitting jobs and, given
the state parameter, has full access to the state of the pipeline, such
as config, options, DRMAA and the logger.
'''

#from pipeline_base.utils import safe_make_dir, run_java
from pipeline_base.stages import Stages

class PipelineStages(Stages):
    def __init__(self, *args, **kwargs):
        super(PipelineStages, self).__init__(*args, **kwargs)
        self.reference = self.get_options('human_reference_genome')


    def original_fastqs(self, output):
        '''Original fastq files'''
        pass

    def human_reference_genome(self, output):
        '''Human reference genome in FASTA format'''
        pass


    def index_ref_bwa(self, reference_in, index_outputs):
        '''Index human genome reference with BWA'''
        command = "bwa index -a bwtsw {reference}".format(reference=reference_in)
        self.run('index_ref_bwa', command)


    def align_bwa(self, inputs, bam_out, sample_id):
        '''Align the paired end fastq files to the reference genome using bwa'''
        fastq_read1_in, fastq_read2_in = inputs
        cores = self.get_stage_options('align_bwa', 'cores')
        read_group = '"@RG\\tID:{sample}\\tSM:{sample}\\tPL:Illumina"'.format(sample=sample_id)
        command = 'bwa mem -t {cores} -R {read_group} {reference} {fastq_read1} {fastq_read2} ' \
                  '| samtools view -b -h -o {bam} -' \
                  .format(cores=cores,
                      read_group=read_group,
                      fastq_read1=fastq_read1_in,
                      fastq_read2=fastq_read2_in,
                      reference=self.reference,
                      bam=bam_out)
        self.run('align_bwa', command)
