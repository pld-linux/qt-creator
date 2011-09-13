Summary:	An IDE tailored to the needs of Qt developers
Summary(pl.UTF-8):	IDE dostosowane do potrzeb developerow Qt
Name:		qt-creator
Version:	2.3.0
Release:	2
Epoch:		1
License:	LGPL v2.1
Group:		X11/Development/Tools
Source0:	http://get.qt.nokia.com/qtcreator/%{name}-%{version}-src.zip
# Source0-md5:	9d0ca1d39cb7f6d54d86d16ba1593b2f
Source1:	%{name}.desktop
Patch0:		%{name}-pluginpath64.patch
URL:		http://qt.nokia.com/products/developer-tools
BuildRequires:	QtDBus-devel
BuildRequires:	QtDeclarative-devel
BuildRequires:	QtDesigner-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtHelp-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtScript-devel
BuildRequires:	QtSql-sqlite3
BuildRequires:	QtSvg-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	QtXml-devel
BuildRequires:	qt4-build >= 4.7.0
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake >= 4.7.0
BuildRequires:	rpmbuild(macros) >= 1.602
BuildRequires:	unzip
Requires(post,postun):	desktop-file-utils
%requires_eq	QtCore
Requires:	QtSql-sqlite3
Requires:	hicolor-icon-theme
# for xdg-open
Suggests:	xdg-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt Creator is a cross-platform integrated development environment (IDE)
tailored to the needs of Qt developers.

%description -l pl.UTF-8
Qt Creator to wieloplatformowe IDE dostosowane do potrzeb developerow Qt.

%prep
%setup -q -n %{name}-%{version}-src

%if "%{_lib}" == "lib64"
%patch0 -p1
%endif

%build
export QTDIR=%{_libdir}/qt4
# the qmakespec in qt4 is somewhat broken, need to look at this
#export QMAKESPEC=%{_datadir}/qt4/mkspecs/linux-g++/

qmake-qt4 qtcreator.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

export QTDIR=%{_libdir}/qt4
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
%{_sysconfdir}/ld.so.conf.d/qtcreator.conf
%dir %{_libdir}/qtcreator
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so.*.*
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so
%attr(755,root,root) %ghost %{_libdir}/qtcreator/lib*.so.1
%dir %{_libdir}/qtcreator/plugins
%dir %{_libdir}/qtcreator/plugins/Nokia
%{_libdir}/qtcreator/plugins/Nokia/*.pluginspec
%attr(755,root,root) %{_libdir}/qtcreator/plugins/Nokia/*.so
%{_libdir}/qtcreator/qtcomponents
%{_datadir}/qtcreator
%{_defaultdocdir}/qtcreator
%{_desktopdir}/qt-creator.desktop
%{_iconsdir}/hicolor/*/*/*.png
