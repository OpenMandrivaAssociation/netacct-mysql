Summary:	Network traffic accounting daemon
Name:		netacct-mysql
Version:	0.78
Release:	%mkrel 14
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


