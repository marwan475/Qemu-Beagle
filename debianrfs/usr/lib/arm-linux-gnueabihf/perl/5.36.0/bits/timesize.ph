require '_h2ph_pre.ph';

no warnings qw(redefine misc);

eval 'sub __TIMESIZE () {32;}' unless defined(&__TIMESIZE);
1;
