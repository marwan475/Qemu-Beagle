require '_h2ph_pre.ph';

no warnings qw(redefine misc);

eval 'sub __HAVE_FLOAT128 () {0;}' unless defined(&__HAVE_FLOAT128);
eval 'sub __HAVE_DISTINCT_FLOAT128 () {0;}' unless defined(&__HAVE_DISTINCT_FLOAT128);
eval 'sub __HAVE_FLOAT64X () {0;}' unless defined(&__HAVE_FLOAT64X);
eval 'sub __HAVE_FLOAT64X_LONG_DOUBLE () {0;}' unless defined(&__HAVE_FLOAT64X_LONG_DOUBLE);
unless(defined(&__ASSEMBLER__)) {
    undef(&__f128) if defined(&__f128);
    undef(&__CFLOAT128) if defined(&__CFLOAT128);
}
require 'bits/floatn-common.ph';
1;
