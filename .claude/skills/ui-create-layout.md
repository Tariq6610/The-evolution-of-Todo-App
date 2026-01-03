# UI: Create Layout

Creates a beautiful, responsive page layout using shadcn/ui components and Tailwind CSS.

## Usage

```
/sp.ui.create-layout <layout-name> --type <layout-type> [--description "<desc>"]
```

## Examples

```bash
# Create dashboard layout
/sp.ui.create-layout Dashboard --type dashboard --description "Main dashboard with sidebar and content area"

# Create authentication layout
/sp.ui.create-layout Auth --type auth --description "Centered card for login/signup"

# Create settings layout
/sp.ui.create-layout Settings --type settings --description "Settings page with navigation sidebar"
```

## Layout Types

| Type | Structure | Use Case |
|------|-----------|----------|
| `dashboard` | Sidebar + Header + Content | Admin panels, dashboards |
| `auth` | Centered card | Login, signup, forgot password |
| `settings` | Navigation + Content | Settings pages |
| `public` | Header + Content | Landing pages, documentation |
| `modal` | Dialog/Sheet | Modal dialogs, panels |

## Layout Creation Rules

1. **File Location**: `apps/002-fullstack-web/frontend/app/(layout-type)/layout.tsx`

2. **Responsive Design**:
   - Mobile-first approach
   - Sidebar collapses on mobile
   - Proper spacing on all breakpoints

3. **Accessibility**:
   - Skip to content link
   - Proper ARIA landmarks
   - Keyboard navigation

4. **Navigation**:
   - Active state indication
   - Mobile menu toggle
   - Focus management

## Example: Dashboard Layout

```tsx
"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Menu } from "lucide-react"

export interface DashboardLayoutProps {
  children: React.ReactNode
}

const navItems = [
  { href: "/dashboard", label: "Overview" },
  { href: "/dashboard/tasks", label: "Tasks" },
  { href: "/dashboard/calendar", label: "Calendar" },
  { href: "/dashboard/analytics", label: "Analytics" },
  { href: "/dashboard/settings", label: "Settings" },
]

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname()
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false)

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile Menu */}
      <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
        <SheetContent side="left" className="w-64 p-0">
          <DashboardNav pathname={pathname} onItemClick={() => setMobileMenuOpen(false)} />
        </SheetContent>
      </Sheet>

      {/* Main Layout */}
      <div className="flex">
        {/* Desktop Sidebar */}
        <aside className="hidden w-64 border-r bg-card lg:block">
          <DashboardNav pathname={pathname} />
        </aside>

        {/* Content Area */}
        <div className="flex-1">
          {/* Mobile Header */}
          <header className="border-b lg:hidden">
            <div className="flex h-16 items-center px-4">
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" onClick={() => setMobileMenuOpen(true)}>
                  <Menu className="h-5 w-5" />
                  <span className="sr-only">Toggle menu</span>
                </Button>
              </SheetTrigger>
              <span className="ml-4 text-lg font-semibold">Dashboard</span>
            </div>
          </header>

          {/* Page Content */}
          <main className="min-h-[calc(100vh-4rem)] p-4 lg:p-8">
            {children}
          </main>
        </div>
      </div>
    </div>
  )
}

function DashboardNav({
  pathname,
  onItemClick,
}: {
  pathname: string
  onItemClick?: () => void
}) {
  return (
    <ScrollArea className="h-full py-4">
      <div className="px-4">
        <Link href="/" className="mb-6 flex items-center space-x-2">
          <Logo />
          <span className="text-lg font-semibold">Todo App</span>
        </Link>
      </div>

      <nav className="space-y-1 px-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href

          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onItemClick}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
              aria-current={isActive ? "page" : undefined}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>
    </ScrollArea>
  )
}

function Logo() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-6 w-6"
    >
      <path d="M12 2L2 7l10 5 10-5-10-5z" />
      <path d="M2 17l10 5 10-5" />
      <path d="M2 12l10 5 10-5" />
    </svg>
  )
}
```

## Example: Auth Layout

```tsx
"use client"

import * as React from "react"
import Link from "next/link"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"

export interface AuthLayoutProps {
  children: React.ReactNode
  title: string
  description?: string
  showBackLink?: boolean
  backLinkText?: string
  backLinkHref?: string
}

export function AuthLayout({
  children,
  title,
  description,
  showBackLink = true,
  backLinkText = "Back to home",
  backLinkHref = "/",
}: AuthLayoutProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background to-muted p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <Link href="/" className="flex justify-center mb-4">
            <Logo />
          </Link>
          <h1 className="text-2xl font-bold text-center">{title}</h1>
          {description && (
            <p className="text-sm text-center text-muted-foreground">
              {description}
            </p>
          )}
        </CardHeader>
        <CardContent>{children}</CardContent>
        {showBackLink && (
          <CardFooter className="flex justify-center">
            <Button variant="ghost" asChild>
              <Link href={backLinkHref}>{backLinkText}</Link>
            </Button>
          </CardFooter>
        )}
      </Card>
    </div>
  )
}

function Logo() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-12 w-12"
    >
      <path d="M12 2L2 7l10 5 10-5-10-5z" />
      <path d="M2 17l10 5 10-5" />
      <path d="M2 12l10 5 10-5" />
    </svg>
  )
}
```

## Layout Components

Use these shadcn/ui components:

| Component | Usage |
|-----------|-------|
| `ScrollArea` | Scrollable content areas |
| `Sheet` | Mobile drawer/sidebar |
| `Dialog` | Modal dialogs |
| `Card` | Content containers |
| `Container` | Max-width container |

## Responsive Breakpoints

```tsx
// Mobile (< 768px)
className="flex flex-col space-y-4"

// Tablet (768px - 1024px)
className="flex flex-col md:flex-row md:space-y-0 md:space-x-4"

// Desktop (>= 1024px)
className="flex flex-col md:flex-row lg:space-x-8"
```

## Checklist

After creating layout, verify:
- [ ] Mobile responsive design
- [ ] Sidebar collapses on mobile
- [ ] Keyboard navigation works
- [ ] Skip to content link included
- [ ] ARIA landmarks present
- [ ] Active state indication in nav
- [ ] Focus management
- [ ] Smooth transitions
- [ ] Proper spacing on all breakpoints
- [ ] Accessible color contrast
