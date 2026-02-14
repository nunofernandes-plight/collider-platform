<template>
  <div id="app">
    <header class="app-header">
      <h1>⚛️ Collider Platform</h1>
      <nav>
        <router-link to="/">Event Display</router-link>
        <router-link to="/analysis">Analysis</router-link>
        <router-link to="/config">Configuration</router-link>
      </nav>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>
    
    <footer class="app-footer">
      <p>Particle Collision Visualization & Analysis Platform | Hackathon MVP</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.app-header h1 {
  margin: 0 0 1rem 0;
  font-size: 2rem;
  font-weight: 700;
}

.app-header nav {
  display: flex;
  gap: 2rem;
}

.app-header nav a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.app-header nav a:hover,
.app-header nav a.router-link-active {
  background: rgba(255, 255, 255, 0.2);
}

.app-main {
  flex: 1;
  padding: 2rem;
}

.app-footer {
  background: #1a1a2e;
  padding: 1rem;
  text-align: center;
  color: #888;
  font-size: 0.875rem;
}
</style>
