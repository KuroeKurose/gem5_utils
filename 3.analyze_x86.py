#!/usr/bin/env python3
from gem5_utils import parse_result, to_csv, generate_plot

# Define benchmark names.
benchmarks = [
      # '400.perlbench',
      # '401.bzip2',
      # '403.gcc',
      # '410.bwaves',
      # '416.gamess',
      '429.mcf',
      #'433.milc',
      #'434.zeusmp',
      #'435.gromacs',
      #'436.cactusADM',
      #'437.leslie3d',
      #'444.namd',
      #'445.gobmk',
      #'450.soplex',
      #'453.povray',
      #'454.calculix',
      #'456.hmmer',
      #'458.sjeng',
      #'459.GemsFDTD',
      #'462.libquantum',
      #'464.h264ref',
      #'470.lbm',
      #'471.omnetpp',
      #'473.astar',
      #'482.sphinx3'
]


# Create CSVs and Figures illustrating the relationship between the L2 Cache Size and the L2 Miss Rate.
def parse_results_l2_prefetchers():
    results = []

    for benchmark in benchmarks:
        for l2_size in ['256kB']:
            for (l2_stride_prefetcher, l2_tagged_prefetcher) in [(False, False), (False, True), (True, False)]:
            # for l2_stride_prefetcher in [False, True]:
            #     for l2_tagged_prefetcher in [False, True]:
                results.append(
                    parse_result('results/' +
                                benchmark + '/' + l2_size + '/8way/' + str(l2_stride_prefetcher)  + '-' + str(l2_tagged_prefetcher) + '/1c/',
                                benchmark=benchmark,
                                l2_size=l2_size,
                                l2_stride_prefetcher=l2_stride_prefetcher,
                                l2_tagged_prefetcher=l2_tagged_prefetcher)
                )

    def l2_prefetchers(r):
        prefetchers = ''

        l2_stride_prefetcher = bool(r.props['l2_stride_prefetcher'])
        l2_tagged_prefetcher = bool(r.props['l2_tagged_prefetcher'])

        if l2_stride_prefetcher:
            prefetchers = prefetchers + '+Stride'
        if l2_tagged_prefetcher:
            prefetchers = prefetchers + '+Tagged'
        if prefetchers == '':
            prefetchers = 'None'

        prefetchers = prefetchers.strip('+')

        return prefetchers

    to_csv('results/l2_prefetchers.csv', results, [
        ('Benchmark', lambda r: r.props['benchmark']),
        # ('L2 Size', lambda r: r.props['l2_size']),
        ('L2 Stride Prefetcher', lambda r: r.props['l2_stride_prefetcher']),
        ('L2 Tagged Prefetcher', lambda r: r.props['l2_tagged_prefetcher']),
        ('L2 Prefetchers', lambda r: l2_prefetchers(r)),
        # ('L1D Prefetcher', lambda r: r.props['l1d_prefetcher']),
        ('L2 Prefetches', lambda r: r.stats[0]['system.l2.prefetcher.num_hwpf_issued']),
        # ('L1D Prefetches', lambda r: r.stats[0]['system.cpu.dcache.prefetcher.num_hwpf_issued']),
        ('L2 Miss Rate', lambda r: r.stats[0]['system.l2.overall_miss_rate::total']),
        # ('L1D Miss Rate', lambda r: r.stats[0]['system.cpu.dcache.overall_miss_rate::total']),

        ('# Cycles', lambda r: r.stats[0]['system.switch_cpus.numCycles'])
    ])

    # generate_plot('results/l2_prefetchers.csv',
    #               'results/l2_sizes_vs_l2_miss_rate.pdf', 'Benchmark', 'L2 Miss Rate',
    #               'L2 Size', 'L2 Miss Rate')
    # generate_plot('results/l2_prefetchers.csv',
    #               'results/l2_sizes_vs_num_cycles.pdf', 'Benchmark', '# Cycles',
    #               'L2 Size', '# Cycles')

    generate_plot('results/l2_prefetchers.csv',
                  'results/l2_prefetchers_vs_l2_prefetches.pdf', 'Benchmark', 'L2 Prefetches',
                   'L2 Prefetchers', 'L2 Prefetches')
    generate_plot('results/l2_prefetchers.csv',
                  'results/l2_prefetchers_vs_l2_miss_rate.pdf', 'Benchmark', 'L2 Miss Rate',
                   'L2 Prefetchers', 'L2 Miss Rate')
    generate_plot('results/l2_prefetchers.csv',
                  'results/l2_prefetchers_vs_num_cycles.pdf', 'Benchmark', '# Cycles',
                   'L2 Prefetchers', '# Cycles')

    return results


# Create CSVs and Figures illustrating the relationship between the L2 Prefetchers and the L2 Miss Rate.
parse_results_l2_prefetchers()
