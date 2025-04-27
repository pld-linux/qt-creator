#
# Conditional build:
%bcond_with	qbs		# package Qbs build tool
%bcond_without	webengine	# QtWebEngine based help viewer

%ifnarch %{x8664} aarch64
%undefine	with_webengine
%endif

%define		qtver	6.4.3

Summary:	An IDE tailored to the needs of Qt developers
Summary(pl.UTF-8):	IDE dostosowane do potrzeb programistów Qt
Name:		qt-creator
Version:	15.0.0
Release:	4
Epoch:		1
License:	LGPL v2.1
Group:		X11/Development/Tools
Source0:	https://download.qt.io/official_releases/qtcreator/15.0/%{version}/%{name}-opensource-src-%{version}.tar.xz
# Source0-md5:	01c2e452721f81d070081eb2f8416ad0
# cd src/libs/gocmdbridge/server
# go mod vendor
# cd ../../../..
# tar acf go-vendor.tar.xz src/libs/gocmdbridge/server/vendor
Source1:	go-vendor.tar.xz
# Source1-md5:	be8524f78f4bff8f151db634c1d7e23d
Patch0:		go-vendor.patch
URL:		https://doc.qt.io/qtcreator/
BuildRequires:	Qt6Concurrent-devel >= %{qtver}
BuildRequires:	Qt6Designer-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Help-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6PrintSupport-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Qt5Compat-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6SerialPort-devel >= %{qtver}
BuildRequires:	Qt6ShaderTools-devel >= %{qtver}
BuildRequires:	Qt6Sql-devel >= %{qtver}
BuildRequires:	Qt6Svg-devel >= %{qtver}
BuildRequires:	Qt6UiTools-devel >= %{qtver}
%{?with_webengine:BuildRequires:	Qt6WebEngine-devel >= %{qtver}}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	clang-devel >= 6.0.0
BuildRequires:	cmake >= 3.20
BuildRequires:	gdb
BuildRequires:	golang >= 1.21.7
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	llvm-devel >= 7.0.0
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	qt6-linguist
BuildRequires:	qt6-shadertools
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	upx >= 3.94
BuildRequires:	xz
BuildRequires:	yaml-cpp-devel >= 0.8
Requires(post,postun):	desktop-file-utils
%requires_eq	Qt6Core
Requires:	Qt6Gui-platform-xcb
Requires:	Qt6Sql-sqldriver-sqlite3
Requires:	hicolor-icon-theme
Requires:	qt5-qtdeclarative
# for xdg-open
Suggests:	xdg-utils
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	'libClangsupport\.so.*'
%define		_noautostrip		.*cmdbridge.*

%description
Qt Creator is a cross-platform integrated development environment
(IDE) tailored to the needs of Qt developers.

%description -l pl.UTF-8
Qt Creator to wieloplatformowe IDE dostosowane do potrzeb programistów
Qt.

%prep
%setup -q -n %{name}-opensource-src-%{version} -a1
%patch -P 0 -p1

sed -i '1s,/usr/bin/env python,%{__python},' src/shared/qbs/src/3rdparty/python/lib/python3.9/site-packages/dmgbuild/__main__.py

%build
%cmake -B build \
	%{cmake_on_off qbs BUILD_QBS} \
	%{cmake_on_off webengine BUILD_HELPVIEWERBACKEND_QTWEBENGINE}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/qtcreator" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/qtcreator.conf
cp -p share/applications/org.qt-project.qtcreator.desktop $RPM_BUILD_ROOT%{_desktopdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/qtcreator/*.prl

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
%if %{with qbs}
%attr(755,root,root) %{_bindir}/qbs
%attr(755,root,root) %{_bindir}/qbs-config
%attr(755,root,root) %{_bindir}/qbs-config-ui
%attr(755,root,root) %{_bindir}/qbs-create-project
%attr(755,root,root) %{_bindir}/qbs-setup-android
%attr(755,root,root) %{_bindir}/qbs-setup-qt
%attr(755,root,root) %{_bindir}/qbs-setup-toolchains
%endif
%attr(755,root,root) %{_bindir}/qtcreator
%{_sysconfdir}/ld.so.conf.d/qtcreator.conf
%dir %{_libexecdir}/qtcreator
%attr(755,root,root) %{_libexecdir}/qtcreator/buildoutputparser
%attr(755,root,root) %{_libexecdir}/qtcreator/cmdbridge-*
%attr(755,root,root) %{_libexecdir}/qtcreator/cpaster
%{?with_qbs:%attr(755,root,root) %{_libexecdir}/qtcreator/dmgbuild}
%attr(755,root,root) %{_libexecdir}/qtcreator/perf2text
%attr(755,root,root) %{_libexecdir}/qtcreator/perfparser
%attr(755,root,root) %{_libexecdir}/qtcreator/qtcreator_processlauncher
%{?with_qbs:%attr(755,root,root) %{_libexecdir}/qtcreator/qbs_processlauncher}
%attr(755,root,root) %{_libexecdir}/qtcreator/qml2puppet-%{version}
%attr(755,root,root) %{_libexecdir}/qtcreator/qtcreator_process_stub
%attr(755,root,root) %{_libexecdir}/qtcreator/qtc-askpass
%attr(755,root,root) %{_libexecdir}/qtcreator/qtpromaker
%attr(755,root,root) %{_libexecdir}/qtcreator/sdktool
%dir %{_libdir}/qtcreator
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/qtcreator/lib*.so.15
%dir %{_libdir}/qtcreator/plugins
%attr(755,root,root) %{_libdir}/qtcreator/plugins/lib*.so
%if %{with qbs}
%dir %{_libdir}/qtcreator/plugins/qbs
%dir %{_libdir}/qtcreator/plugins/qbs/plugins
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libclangcompilationdbgenerator.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libiarewgenerator.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libkeiluvgenerator.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libmakefilegenerator.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libqbs_cpp_scanner.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libqbs_qt_scanner.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libvisualstudiogenerator.so
%endif
%dir %{_libdir}/qtcreator/plugins/qmldesigner
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qmldesigner/libassetexporterplugin.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qmldesigner/libcomponentsplugin.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qmldesigner/libqmlpreviewplugin.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qmldesigner/libqtquickplugin.so
%{_datadir}/qtcreator
%{_datadir}/metainfo/org.qt-project.qtcreator.appdata.xml
%{_desktopdir}/org.qt-project.qtcreator.desktop
%{_iconsdir}/hicolor/*x*/apps/QtProject-qtcreator.png
