import { Component, OnInit, output } from '@angular/core';
import { HttpClient, HttpHeaders  } from '@angular/common/http';
import { CommonModule } from '@angular/common';
//import Chart from 'chart.js/auto';

@Component({
  selector: 'app-home',
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent   {

  output: any = null;
  chart: any;
  constructor(private http: HttpClient) {}
  
  ngOnInit(): void {
    interface StatusRow {
      [key: string]: any;
    }
    interface StatusResponse {
      result: StatusRow[];
    }
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = {}
    this.http.post<StatusResponse>('http://127.0.0.1:5000/api/sim_dashboard/status', body, { headers })
      .subscribe({
        next: (response) => {
          this.output = response.result;
          
          console.log('Home data:', this.output);
        },
        error: (err) => {
          console.error('Data loading error:', err);
        }
      });
}

}
