# Copyright 2016-2020 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.required_version('>=2.14')
@rfm.simple_test
class GpuDirectCudaCheck(rfm.RegressionTest):
    def __init__(self):
        self.descr = 'tests gpu-direct for CUDA'
        self.valid_systems = ['daint:gpu', 'dom:gpu', 'kesch:cn',
                              'tiger:gpu', 'arolla:cn', 'tsa:cn']
        self.valid_prog_environs = ['PrgEnv-gnu']
        self.sourcepath = 'gpu_direct_cuda.cu'
        self.build_system = 'SingleSource'
        self.build_system.ldflags = ['-lcublas', '-lcudart']
        if self.current_system.name in ['daint', 'dom', 'tiger']:
            self.modules = ['craype-accel-nvidia60']
            self.variables = {'MPICH_RDMA_ENABLED_CUDA': '1'}
            self.build_system.cxxflags = ['-ccbin CC', '-arch=sm_60']
        elif self.current_system.name == 'kesch':
            self.exclusive_access = True
            self.valid_prog_environs = ['PrgEnv-gnu']
            self.modules = ['cudatoolkit/8.0.61']
            self.variables = {
                'MV2_USE_CUDA': '1',
                'G2G': '1',
            }
            self.build_system.cxxflags = ['-ccbin', 'mpicxx', '-arch=sm_37']
        elif self.current_system.name in ['arolla', 'tsa']:
            self.exclusive_access = True
            self.valid_prog_environs = ['PrgEnv-gnu']
            self.variables = {
                'G2G': '1',
            }
            self.build_system.cxxflags = ['-ccbin', 'mpicxx', '-arch=sm_70']

        self.num_tasks = 2
        self.num_gpus_per_node = 1
        self.num_tasks_per_node = 1
        result = sn.extractsingle(r'Result :\s+(?P<result>\d+\.?\d*)',
                                  self.stdout, 'result', float)
        self.sanity_patterns = sn.assert_reference(result, 1., -1e-5, 1e-5)
        self.maintainers = ['AJ', 'MKr']
        self.tags = {'production', 'mch', 'craype'}
