#
# Conditional build:
%bcond_without	apidocs         # disable gtk-doc
%bcond_without	static_libs	# don't build static library

%define		dbus_version	1.2.16
%define		expat_version	1:1.95.5
%define		glib2_version	1:2.26
Summary:	GLib-based library for using D-BUS
Summary(pl.UTF-8):	Biblioteka do używania D-BUS oparta o GLib
Name:		dbus-glib
Version:	0.102
Release:	2
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
# Source0-md5:	f76b8558fd575d0106c3a556eaa49184
Patch0:		%{name}-configure.patch
URL:		http://www.freedesktop.org/Software/DBusBindings
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= %{dbus_version}
%{?with_apidocs:BuildRequires:	docbook-dtd412-xml}
BuildRequires:	expat-devel >= %{expat_version}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= %{glib2_version}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.8}
%{?with_apidocs:BuildRequires:	gtk-doc-automake >= 1.8}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
Requires:	dbus-libs >= %{dbus_version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS add-on library to integrate the standard D-BUS library with the
GLib thread abstraction and main loop.

%description -l pl.UTF-8
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z abstrakcją wątków i główną pętlą GLib.

%package devel
Summary:	Header files for GLib-based library for using D-BUS
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki do używania D-BUS opartej o GLib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel >= %{dbus_version}
Requires:	glib2-devel >= %{glib2_version}

%description devel
Header files for GLib-based library for using D-BUS.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki do używania D-BUS opartej o GLib.

%package static
Summary:	Static GLib-based library for using D-BUS
Summary(pl.UTF-8):	Statyczna biblioteka do używania D-BUS oparta o GLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GLib-based library for using D-BUS.

%description static -l pl.UTF-8
Statyczna biblioteka do używania D-BUS oparta o GLib.

%package apidocs
Summary:	D-BUS-GLib API documentation
Summary(pl.UTF-8):	Dokumentacja API D-BUS-GLib
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
D-BUS-GLib API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API D-BUS-GLib.

%package -n bash-completion-dbus
Summary:	bash-completion for dbus-send
Summary(pl.UTF-8):	Bashowe uzupełnianie poleceń dla dbus-send
Group:		Applications/Shells
Requires:	bash-completion

%description -n bash-completion-dbus
This package provides bash-completion for dbus-send.

%description -n bash-completion-dbus -l pl.UTF-8
Ten pakiet dostarcza bashowe uzupełnianie poleceń dla dbus-send.

%prep
%setup -q
%patch0 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__disable apidocs gtk-doc} \
	%{__disable static_libs static} \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	profiledir=/etc/bash_completion.d

mv -f $RPM_BUILD_ROOT/etc/bash_completion.d/{dbus-bash-completion.sh,dbus}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# AFL not in common-licenses, so COPYING included
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdbus-glib-1.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-binding-tool
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so
%{_libdir}/libdbus-glib-1.la
%{_mandir}/man1/dbus-binding-tool.1*
%{_includedir}/dbus-1.0/dbus/dbus-glib*.h
%{_includedir}/dbus-1.0/dbus/dbus-gtype-specialized.h
%{_includedir}/dbus-1.0/dbus/dbus-gvalue-parse-variant.h
%{_pkgconfigdir}/dbus-glib-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-glib-1.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dbus-glib
%endif

%files -n bash-completion-dbus
%defattr(644,root,root,755)
/etc/bash_completion.d/dbus
%attr(755,root,root) %{_libdir}/dbus-bash-completion-helper
