#!/bin/sh
#Submit using flux batch <filename>

#flux: --job-name=c5ce_surface
#flux: --output='c5ce.{{id}}.out'
#flux: --error='c5c3.{{id}}.err'
#flux: -N 1
#flux: -l # Add task rank prefixes to each line of output.
#flux: --setattr=thp=always # Enable Transparent Huge Pages (THP)
#flux: -t 20
#flux: -q pbatch # other available queues: pdebug

export MPICH_GPU_SUPPORT_ENABLED=0 # for NVIDIA only
export HSA_XNACK=1

export MCDC_XSLIB=/usr/workspace/morgan83/lassen_dep/MCDC/MCDC-Xsec/mcdc_xs
module load rocm/6.0.0
source /usr/workspace/morgan83/tuo_dep/venv-tuo/bin/activate


cp ../../input.py .

# Check if THP are enabled
#cat /sys/kernel/mm/transparent_hugepage/enabled

flux run -N 1 -n 4 -g 1 python input.py --no-progress_bar --mode=numba --target=gpu --output surface_c5ce_tuo

#flux run -N1 -n4 -x -l -g1  ./example
#flux run -N1 -n4 -x -l -g1  ./example