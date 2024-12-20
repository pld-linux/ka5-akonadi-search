# TODO: Corrosion https://github.com/corrosion-rs/corrosion
#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeappsver	%{version}
# packages version, not cmake config version (which is 5.24.5)
%define		ka_ver		%{version}
%define		kf_ver		5.105.0
%define		qt_ver		5.15.2
%define		kaname		akonadi-search
Summary:	Akonadi Search
Summary(pl.UTF-8):	Komponent wyszukiwania dla Akonadi
Name:		ka5-%{kaname}
Version:	23.08.5
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	6b7a2c0afc7d235e51d3294ff5b3a684
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Test-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka5-akonadi-devel >= %{ka_ver}
BuildRequires:	ka5-akonadi-mime-devel >= %{ka_ver}
BuildRequires:	ka5-kmime-devel >= %{ka_ver}
BuildRequires:	kf5-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf5-kcalendarcore-devel >= %{kf_ver}
BuildRequires:	kf5-kcmutils-devel >= %{kf_ver}
BuildRequires:	kf5-kconfig-devel >= %{kf_ver}
BuildRequires:	kf5-kconfigwidgets-devel >= %{kf_ver}
BuildRequires:	kf5-kcontacts-devel >= %{kf_ver}
BuildRequires:	kf5-kcrash-devel >= %{kf_ver}
BuildRequires:	kf5-kdbusaddons-devel >= %{kf_ver}
BuildRequires:	kf5-ki18n-devel >= %{kf_ver}
BuildRequires:	kf5-kio-devel >= %{kf_ver}
BuildRequires:	kf5-krunner-devel >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xapian-core-devel
BuildRequires:	xz
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5Gui >= %{qt_ver}
Requires:	ka5-akonadi >= %{ka_ver}
Requires:	ka5-akonadi-mime >= %{ka_ver}
Requires:	ka5-kmime >= %{ka_ver}
Requires:	kf5-kcalendarcore >= %{kf_ver}
Requires:	kf5-kconfig >= %{kf_ver}
Requires:	kf5-kcontacts >= %{kf_ver}
Requires:	kf5-ki18n >= %{kf_ver}
Requires:	kf5-krunner >= %{kf_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries and daemons to implement searching in Akonadi.

%description -l pl.UTF-8
Biblioteki i demony do implementowania wyszukiwania w Akonadi.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	ka5-akonadi-devel >= %{ka_ver}
Requires:	ka5-akonadi-mime-devel >= %{ka_ver}
Requires:	ka5-kmime-devel >= %{ka_ver}
Requires:	kf5-kcalendarcore-devel >= %{kf_ver}
Requires:	kf5-kcontacts-devel >= %{kf_ver}
Requires:	kf5-kcoreaddons-devel >= %{kf_ver}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang akonadi_search

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f akonadi_search.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/akonadi_indexing_agent
%attr(755,root,root) %{_bindir}/akonadi_html_to_text
%attr(755,root,root) %{_libdir}/libKPim5AkonadiSearchCore.so.*.*.*
%ghost %{_libdir}/libKPim5AkonadiSearchCore.so.5
%attr(755,root,root) %{_libdir}/libKPim5AkonadiSearchDebug.so.*.*.*
%ghost %{_libdir}/libKPim5AkonadiSearchDebug.so.5
%attr(755,root,root) %{_libdir}/libKPim5AkonadiSearchPIM.so.*.*.*
%ghost %{_libdir}/libKPim5AkonadiSearchPIM.so.5
%attr(755,root,root) %{_libdir}/libKPim5AkonadiSearchXapian.so.*.*.*
%ghost %{_libdir}/libKPim5AkonadiSearchXapian.so.5
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/krunner/krunner_pimcontacts.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/krunner/kcms/kcm_krunner_pimcontacts.so
%attr(755,root,root) %{_libdir}/qt5/plugins/pim5/akonadi/akonadi_search_plugin.so
%attr(755,root,root) %{_libdir}/qt5/plugins/pim5/akonadi/calendarsearchstore.so
%attr(755,root,root) %{_libdir}/qt5/plugins/pim5/akonadi/contactsearchstore.so
%attr(755,root,root) %{_libdir}/qt5/plugins/pim5/akonadi/emailsearchstore.so
%attr(755,root,root) %{_libdir}/qt5/plugins/pim5/akonadi/notesearchstore.so
%{_datadir}/akonadi/agents/akonadiindexingagent.desktop
%{_datadir}/qlogging-categories5/akonadi-search.categories
%{_datadir}/qlogging-categories5/akonadi-search.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKPim5AkonadiSearchCore.so
%{_libdir}/libKPim5AkonadiSearchDebug.so
%{_libdir}/libKPim5AkonadiSearchPIM.so
%{_libdir}/libKPim5AkonadiSearchXapian.so
%{_includedir}/KPim5/AkonadiSearch
%{_libdir}/cmake/KPim5AkonadiSearch
