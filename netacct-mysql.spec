Summary:	Network traffic accounting daemon
Name:		netacct-mysql
Version:	0.78
Release:	15
License:	GPL
Group:		System/Servers
URL:		http://netacct-mysql.gabrovo.com/
Source0:	http://netacct-mysql.gabrovo.com/download/%{name}-%{version}.tar.bz2
Patch0:		%{name}-initscript.patch
Patch1:		netacct-mysql-lib64_shared.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	mysql-devel
BuildRequires:	libpcap-devel >= 0.7
BuildRequires:	automake
BuildRequires:	autoconf2.5
BuildRequires:	chrpath
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Traffic Accounting Daemon with mysql support Network traffic
accounting daemon which stores data in mysql. Support for per hour
statistics, peering/international traffic accounting.

%prep

%setup -q
%patch0 -p0
%patch1 -p0

%build
rm -f configure
libtoolize --copy --force; aclocal; automake --add-missing --copy; autoconf --force

export LIBS="$LIBS -L%{_libdir} -lmysqlclient"

%configure2_5x \
    --with-mysql=%{_prefix}

%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

%makeinstall_std

install -d %{buildroot}%{_initrddir}
install -m0755 contrib/nacctd.redhat %{buildroot}%{_initrddir}/%{name}

# nuke rpath
chrpath -d %{buildroot}%{_sbindir}/nacctd

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS FAQ INSTALL NEWS README* TODO netacct.sql contrib/nacctpeering.*
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nacctpeering
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/naccttab
%{_mandir}/man8/nacctd.8*
%{_mandir}/man8/nacctpeering.8*
%{_sbindir}/nacctd




%changelog
* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 0.78-14mdv2011.0
+ Revision: 645849
- relink against libmysqlclient.so.18

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.78-13mdv2011.0
+ Revision: 627811
- don't force the usage of automake1.7

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 0.78-12mdv2011.0
+ Revision: 627267
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.78-11mdv2011.0
+ Revision: 626548
- rebuilt against mysql-5.5.8 libs

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 0.78-9mdv2011.0
+ Revision: 613012
- the mass rebuild of 2010.1 packages

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 0.78-8mdv2010.1
+ Revision: 507494
- rebuild

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 0.78-7mdv2010.0
+ Revision: 440247
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - use lowercase mysql-devel

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.78-6mdv2009.1
+ Revision: 311312
- rebuilt against mysql-5.1.30 libs

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.78-5mdv2009.1
+ Revision: 298318
- rebuilt against libpcap-1.0.0

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 0.78-4mdv2009.0
+ Revision: 253752
- rebuild

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 0.78-2mdv2008.1
+ Revision: 140994
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Feb 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.78-2mdv2007.0
+ Revision: 116082
- bump release
- added P1 (lib64 and shared fixes)
- Import netacct-mysql

* Thu Jan 12 2006 Oden Eriksson <oeriksson@mandriva.com> 0.78-1mdk
- 0.78

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.76-4mdk
- rebuilt against MySQL-5.0.15

* Thu Jul 14 2005 Oden Eriksson <oeriksson@mandriva.com> 0.76-3mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Tue Jan 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.76-2mdk
- rebuilt against MySQL-4.1.x system libs

* Mon May 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.76-1mdk
- 0.76
- new url, fix deps, use macros
- drop P1, it's included

