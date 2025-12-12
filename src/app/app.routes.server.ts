import { RenderMode, ServerRoute } from '@angular/ssr';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Dashboard1Component } from './components/dashboard1/dashboard1.component';
import { HomeComponent } from './components/home/home.component';
import { SimDashboardComponent } from './components/gbts-simulator-dashboard/gbts-simulator-dashboard.component';

export const serverRoutes: ServerRoute[] = [
  {
    path: '**',
    renderMode: RenderMode.Prerender
  }
];

const routes: Routes = [
  { path: 'dashboard1', component: Dashboard1Component },
  {path: 'home', component: HomeComponent},
  {path: 'sim-dashboard', component: SimDashboardComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
