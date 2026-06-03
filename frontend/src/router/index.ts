import { createRouter, createWebHistory } from 'vue-router'

const DEFAULT_TITLE = 'TapeForge Dock'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/overview' },
    {
      path: '/overview',
      name: 'overview',
      component: () => import('../views/OverviewView.vue'),
      meta: { label: 'Overview' },
    },
    {
      path: '/sessions',
      name: 'sessions',
      component: () => import('../views/SessionsView.vue'),
      meta: { label: 'Sessions' },
    },
    {
      path: '/sessions/:id',
      name: 'session-detail',
      component: () => import('../views/SessionDetailView.vue'),
      meta: { label: 'Sessions' },
    },
    {
      path: '/systems/:id?',
      name: 'systems',
      component: () => import('../views/SystemsView.vue'),
      meta: { label: 'Systems' },
    },
    {
      path: '/crew',
      name: 'crew',
      component: () => import('../views/CrewView.vue'),
      meta: { label: 'Crew', full: true },
    },
    {
      path: '/knowledge',
      name: 'knowledge',
      component: () => import('../views/KnowledgeView.vue'),
      meta: { label: 'Knowledge' },
    },
    {
      path: '/docs/:slug(.*)?',
      name: 'docs',
      component: () => import('../views/DocumentationView.vue'),
      meta: { label: 'Documentation', full: true },
    },
    {
      path: '/diagnostics',
      name: 'diagnostics',
      component: () => import('../views/DiagnosticsView.vue'),
      meta: { label: 'Diagnostics' },
    },
    { path: '/:pathMatch(.*)*', redirect: '/overview' },
  ],
})

router.afterEach((to) => {
  // DocumentationView sets a per-page title itself; don't clobber it here.
  if (to.name === 'docs') return
  const label = to.meta.label as string | undefined
  document.title = label ? `${label} — TapeForge Dock` : DEFAULT_TITLE
})

export default router
