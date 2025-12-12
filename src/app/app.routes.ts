import { Routes } from '@angular/router';
import { Dashboard1Component } from './components/dashboard1/dashboard1.component';
import { HomeComponent  } from './components/home/home.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { SimDashboardComponent } from './components/gbts-simulator-dashboard/gbts-simulator-dashboard.component';

import path from 'path';
export const routes: Routes = [
  { path: 'home', component: HomeComponent  },
  { path: 'dashboard1', component: Dashboard1Component },
  {path: 'sim-dashboard', component: SimDashboardComponent },
  
  { path: '**', redirectTo: 'home' }
  
];
