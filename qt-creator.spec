Summary:	An IDE tailored to the needs of Qt developers
Summary(pl.UTF-8):	IDE dostosowane do potrzeb developerow Qt
Name:		qt-creator
Version:	3.4.1
Release:	1
Epoch:		1
License:	LGPL v2.1
Group:		X11/Development/Tools
Source0:	http://download.qt-project.org/official_releases/qtcreator/3.4/%{version}/%{name}-opensource-src-%{version}.tar.gz
# Source0-md5:	bcbae4a567c93158babe3b7f42d01219
Source1:	%{name}.desktop
Patch0:		%{name}-pluginpath64.patch
URL:		http://qt.digia.com/Product/Developer-Tools
BuildRequires:	Qt5Declarative-devel >= 5.3.1
BuildRequires:	Qt5Designer-devel >= 5.3.1
BuildRequires:	Qt5Gui-devel >= 5.3.1
BuildRequires:	Qt5Help-devel >= 5.3.1
BuildRequires:	Qt5Network-devel >= 5.3.1
BuildRequires:	Qt5Script-devel >= 5.3.1
BuildRequires:	Qt5Svg-devel >= 5.3.1
BuildRequires:	Qt5WebKit-devel >= 5.3.1
BuildRequires:	Qt5Xml-devel >= 5.3.1
BuildRequires:	gdb
BuildRequires:	qt5-build >= 5.3.1
BuildRequires:	qt5-linguist
BuildRequires:	qt5-qmake >= 5.3.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.602
Requires(post,postun):	desktop-file-utils
%requires_eq	Qt5Core
Requires:	Qt5Sql
Requires:	hicolor-icon-theme
# for xdg-open
Suggests:	xdg-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt Creator is a cross-platform integrated development environment
(IDE) tailored to the needs of Qt developers.

%description -l pl.UTF-8
Qt Creator to wieloplatformowe IDE dostosowane do potrzeb developerow
Qt.

%prep
%setup -q -n %{name}-opensource-src-%{version}

%if "%{_lib}" == "lib64"
%patch0 -p1
%endif

# fix unresolved symbols in libQtcSsh
echo "LIBS += -ldl" > src/libs/ssh/ssh_dependencies.pri

%build
export QTDIR=%{_libdir}/qt5
# the qmakespec in qt4 is somewhat broken, need to look at this
#export QMAKESPEC=%{_datadir}/qt4/mkspecs/linux-g++/

qmake-qt5 qtcreator.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

export QTDIR=%{_libdir}/qt5
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix}

%if "%{_lib}" == "lib64"
mv -f $RPM_BUILD_ROOT{%{_prefix}/lib,%{_libdir}}
%endif

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/qtcreator" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/qtcreator.conf

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# not supported by hicolor-icon-theme
rm -rf $RPM_BUILD_ROOT%{_iconsdir}/hicolor/512x512

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qtcreator
%attr(755,root,root) %{_bindir}/qtcreator_process_stub
%attr(755,root,root) %{_bindir}/qtpromaker
%attr(755,root,root) %{_bindir}/sdktool
%{_sysconfdir}/ld.so.conf.d/qtcreator.conf
%dir %{_libdir}/qtcreator
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so.*.*
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so
%attr(755,root,root) %ghost %{_libdir}/qtcreator/lib*.so.1
%dir %{_libdir}/qtcreator/plugins
%dir %{_libdir}/qtcreator/plugins/BlackBerry
%dir %{_libdir}/qtcreator/plugins/QtProject
%{_libdir}/qtcreator/plugins/BlackBerry/*.pluginspec
%{_libdir}/qtcreator/plugins/QtProject/*.pluginspec
%attr(755,root,root) %{_libdir}/qtcreator/plugins/BlackBerry/*.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/QtProject/*.so
%{_libdir}/qtcreator/qtcomponents
%{_datadir}/qtcreator
%{_desktopdir}/qt-creator.desktop
%{_iconsdir}/hicolor/*/*/*.png
