import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { SimDashboardComponent } from './components/gbts-simulator-dashboard/gbts-simulator-dashboard.component';
import { Dashboard1Component } from './components/dashboard1/dashboard1.component';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'sim-dashboard', component: SimDashboardComponent },
  { path: 'dashboard1', component: Dashboard1Component },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', redirectTo: 'home' }
];