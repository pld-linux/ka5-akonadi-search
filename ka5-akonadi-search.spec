#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	22.08.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		akonadi-search
Summary:	Akonadi Search
Name:		ka5-%{kaname}
Version:	22.08.1
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	482845d0796181ae6da91da7842afd7b
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= 5.9.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	ka5-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka5-akonadi-mime-devel >= %{kdeappsver}
BuildRequires:	ka5-kmime-devel >= %{kdeappsver}
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf5-kcmutils-devel >= %{kframever}
BuildRequires:	kf5-kconfig-devel >= %{kframever}
BuildRequires:	kf5-kcontacts-devel >= %{kframever}
BuildRequires:	kf5-kcrash-devel >= %{kframever}
BuildRequires:	kf5-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	kf5-kio-devel >= %{kframever}
BuildRequires:	kf5-krunner-devel >= %{kframever}
BuildRequires:	kf5-plasma-framework-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xapian-core-devel
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries and daemons to implement searching in Akonadi.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/akonadi_indexing_agent
%ghost %{_libdir}/libKF5AkonadiSearchCore.so.5
%attr(755,root,root) %{_libdir}/libKF5AkonadiSearchCore.so.*.*.*
%ghost %{_libdir}/libKF5AkonadiSearchDebug.so.5
%attr(755,root,root) %{_libdir}/libKF5AkonadiSearchDebug.so.*.*.*
%ghost %{_libdir}/libKF5AkonadiSearchPIM.so.5
%attr(755,root,root) %{_libdir}/libKF5AkonadiSearchPIM.so.*.*.*
%ghost %{_libdir}/libKF5AkonadiSearchXapian.so.5
%attr(755,root,root) %{_libdir}/libKF5AkonadiSearchXapian.so.*.*.*
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/krunner/krunner_pimcontacts.so
%{_datadir}/akonadi/agents/akonadiindexingagent.desktop
%{_datadir}/qlogging-categories5/akonadi-search.categories
%{_datadir}/qlogging-categories5/akonadi-search.renamecategories
%{_libdir}/qt5/plugins/kf5/krunner/kcms/kcm_krunner_pimcontacts.so
%{_libdir}/qt5/plugins/pim5/akonadi/akonadi_search_plugin.so
%{_libdir}/qt5/plugins/pim5/akonadi/calendarsearchstore.so
%{_libdir}/qt5/plugins/pim5/akonadi/contactsearchstore.so
%{_libdir}/qt5/plugins/pim5/akonadi/emailsearchstore.so
%{_libdir}/qt5/plugins/pim5/akonadi/notesearchstore.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/AkonadiSearch
%{_libdir}/cmake/KF5AkonadiSearch
%{_libdir}/libKF5AkonadiSearchCore.so
%{_libdir}/libKF5AkonadiSearchDebug.so
%{_libdir}/libKF5AkonadiSearchPIM.so
%{_libdir}/libKF5AkonadiSearchXapian.so
