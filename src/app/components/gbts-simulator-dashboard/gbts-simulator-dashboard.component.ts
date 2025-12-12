import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sim-dashboard',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './gbts-simulator-dashboard.component.html',
  styleUrls: ['./gbts-simulator-dashboard.component.css']
})
export class SimDashboardComponent {

  Array = Array;

  year: number = 2025;
  week: number = 1;
  month: number = 1;

  output: any = null;
  groupedByWeek: any = {};
  loading = false;
  modes = ['day', 'week', 'month', 'year'];
  selectedMode = 'day';


  startDate = '';
  endDate = '';

  startWeek = 1;
  endWeek = 1;

  startMonth = 1;
  endMonth = 1;

  startYear = new Date().getFullYear();
  endYear = new Date().getFullYear();
  constructor(private http: HttpClient) {}

  getKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }

  private isFullDate(key: string): boolean {
    // Formato YYYY-MM-DD
    return /^\d{4}-\d{2}-\d{2}$/.test(key);
  }

  private calculateWeek(dateStr: string): number {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return -1;

    const oneJan = new Date(date.getFullYear(), 0, 1);
    const day = Math.floor((date.getTime() - oneJan.getTime()) / 86400000);

    return Math.ceil((day + oneJan.getDay() + 1) / 7);
  }

  private prepareGroupedByWeek() {
    const result = this.output?.result;
    if (!result) return;

    const grouped: any = {};

    Object.keys(result).forEach(dateKey => {
      const data = result[dateKey];

      // Calcola la settimana solo se è una data valida
      let week: string | number;

      if (this.isFullDate(dateKey)) {
        week = this.calculateWeek(dateKey);
        }
      else {
        week = "NO_WEEK"; 
      }

      if (!grouped[week]) grouped[week] = [];

      grouped[week].push({
        date: dateKey,
        data: data
      });
    });

    this.groupedByWeek = grouped;
    console.log('Grouped by week:', this.groupedByWeek);
  }

  sendParams() {
    this.loading = true;
    
    
    let params: any = { mode: this.selectedMode };

    if (this.selectedMode === 'day') {
      params.start = this.startDate;
      params.end = this.endDate;
    }

    else if (this.selectedMode === 'week') {
      params.start = this.startWeek;
      params.end = this.endWeek;
    }

    else if (this.selectedMode === 'month') {
      params.start = this.startMonth;
      params.end = this.endMonth;
    }

    else if (this.selectedMode === 'year') {
      params.start = this.startYear;
      params.end = this.endYear;
    }

    this.http.post('http://127.0.0.1:5000/api/sim_dashboard', params, {
  headers: { 'Content-Type': 'application/json' }
})
      .subscribe(
       {
        next: (res) => {
          console.log(res);
          this.output = res;
          this.prepareGroupedByWeek();
          this.loading = false;
        },
        error: (err) => {
          this.output = err;
          this.loading = false;
        }
      });
  }
}
