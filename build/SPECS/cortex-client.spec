%define python_sitelib %(env python2.6 -c 'from distutils import sysconfig; print sysconfig.get_python_lib()')

Name:           cortex-client
Version:        0.1.1
Release:        1
Summary:        Cortex command line client and python library.
Group:          System Environment/Applications
License:        Guardis specific
URL:            http://www.guardis.com/
Packager: 	Sebastien Caps <sebastien.caps@guardis.com>
Vendor: 	Guardis, http://www.guardis.com/
Source0:	cortex-client-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires: 	/usr/bin/python2.6
BuildRequires:  /usr/bin/python2.6

%description
Cortex automates the management of an Information System through the entire lifecycle. 
Integrating in particular the management of virtual machines (though an hypervisor), 
the provisioning, the configuration management, auditing and monitoring.

Copyright 2010 Guardis Sprl, Liège, Belgium.

This software cannot be used and/or distributed without prior authorization from Guardis.

%prep
%setup -c
%{__mkdir} -p %{buildroot}/%{python_sitelib}/cortex_client
%{__mkdir} -p %{buildroot}/%{_bindir}

%install
echo "cortex_client" > %{buildroot}/%{python_sitelib}/cortex_client.pth
%{__cp} -r lib/* %{buildroot}/%{python_sitelib}/cortex_client/

# To be cleaned
# Patching the /usr/bin/cortex file to be able to load the good python version and to load his library
cat cortex | sed -e 's,#!/usr/bin/env python,#!/usr/bin/env python2.6,g' -e "s/sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))/# sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))/g" > cortex.1

%{__mv} cortex.1 %{buildroot}/%{_bindir}/cortex
%{__chmod} 0755 %{buildroot}/%{_bindir}/cortex

%post
rm -rf %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,-)
%doc README
%doc templates*
%{python_sitelib}/*
%attr(0755,root,root) %{_bindir}/cortex

%changelog
* Wed Dec 08 2010 Sebastien Caps <sebastien.caps@guardis.com> - 0.1.1
- Spec file changed to be integrated into github
* Mon Dec 06 2010 Sebastien Caps <sebastien.caps@guardis.com> - 0.1
- Initial package
