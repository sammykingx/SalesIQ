// export const navManifest = [
//     { group: 'Dashboards', label: 'Sales', href: '/dashboards/sales/' },
//     { group: 'Dashboards', label: 'Analytics', href: '/dashboards/analytics/' },
//     { group: 'Dashboards', label: 'CRM Dashboard', href: '/crm/' },
//     { group: 'Apps', label: 'Email', href: '/apps/email/' },
//     { group: 'Apps', label: 'Chat', href: '/apps/chat/' },
//     { group: 'Apps', label: 'Calendar', href: '/apps/calendar/' },
//     { group: 'Apps', label: 'Kanban', href: '/apps/kanban/' },
//     { group: 'Apps', label: 'File Manager', href: '/apps/files/' },
//     { group: 'Apps', label: 'Contacts', href: '/apps/contacts/' },
//     { group: 'Pages', label: 'View Profile', href: '/account/profile/' },
//     { group: 'Pages', label: 'Account Settings', href: '/account/settings/' },
//     { group: 'Pages', label: 'Support', href: '/account/support/' },
//     { group: 'Actions', label: 'Toggle dark mode', action: 'toggleTheme' },
// ];

export const navManifest = [
    { group: 'Main', label: 'Dashboard', href: '/dashboard/' },

    { group: 'Business', label: 'Sales', href: 'invoices/sales/' },
    { group: 'Business', label: 'Record a sale', href: 'invoices/record-sale/' },
    { group: 'Business', label: 'Update Business Socials', href: '/accounts/settings/#socials' },

    { group: 'Management', label: 'All customers', href: '/customers/' },
    { group: 'Management', label: 'All products', href: '/products/' },


    { group: 'Personal', label: 'Your profile', href: '/accounts/profile/' },
    { group: 'Personal', label: 'Update profile info', href: '/accounts/settings/#profile' },
    { group: 'Personal', label: 'Update password', href: '/accounts/settings/#update-password' },

    { group: 'Actions', label: 'Toggle dark mode', action: 'toggleTheme' },
    { group: 'Actions', label: 'Log Out', action: 'logout' },
];