from common.constants import (
    ATT_LANG,
    INTEL_LANG,
    MIPS_ASM,
    MIPS_MML,
    RISCV,
)


def assembly_constants(request):
    return {
        'INTEL_LANG': INTEL_LANG,
        'ATT_LANG': ATT_LANG,
        'MIPS_ASM': MIPS_ASM,
        'MIPS_MML': MIPS_MML,
        'RISCV': RISCV,
    }
