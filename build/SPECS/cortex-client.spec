%define python_sitelib %(env python -c 'from distutils import sysconfig; print sysconfig.get_python_lib()')

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
Requires: 	/usr/bin/python
BuildRequires:  /usr/bin/python

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
%{__mkdir} -p %{buildroot}/usr/lib/%{name}-%{version}/

%install
echo "cortex_client" > %{buildroot}/%{python_sitelib}/cortex_client.pth

# To be cleaned
# Patching the lib/control/files.py and lib/control/resource.py to be able to load the good templates files
cat lib/control/files.py | sed -e  "s/TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates'))/TEMPLATE_DIR = '\/usr\/lib\/%{name}-%{version}\/templates'/g" > lib/control/files.py.1
cat lib/control/resource.py | sed -e "s/TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates'))/TEMPLATE_DIR = '\/usr\/lib\/%{name}-%{version}\/templates'/g" > lib/control/resource.py.1
%{__rm} -f lib/control/files.py
%{__rm} -f lib/control/resource.py
%{__mv} lib/control/files.py.1 lib/control/files.py
%{__mv} lib/control/resource.py.1 lib/control/resource.py

%{__cp} -r lib/* %{buildroot}/%{python_sitelib}/cortex_client/

# To be cleaned
# Patching the /usr/bin/cortex file to be able to load the good python version and to load his library
cat cortex | sed -e "s/sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))/# sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))/g" > cortex.1

%{__mv} cortex.1 %{buildroot}/%{_bindir}/cortex
%{__chmod} 0755 %{buildroot}/%{_bindir}/cortex

%{__cp} -r templates %{buildroot}/usr/lib/%{name}-%{version}/

%post
rm -rf %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,-)
%doc README
%defattr(0755,root,root)
/usr/lib/%{name}-%{version}/templates*
%{python_sitelib}/*
%{_bindir}/cortex

%changelog
* Thu Jan 20 2011 Sebastien Caps <sebastien.caps@guardis.com> - 0.1.1
- fix/remove python2.6 dependencies 
* Wed Dec 08 2010 Sebastien Caps <sebastien.caps@guardis.com> - 0.1.1
- Spec file changed to be integrated into github
* Mon Dec 06 2010 Sebastien Caps <sebastien.caps@guardis.com> - 0.1
- Initial package
