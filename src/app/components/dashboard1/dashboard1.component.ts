import { Component } from '@angular/core';
import { ScriptService } from '../../services/script.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';



@Component({
  selector: 'app-dashboard1',
  standalone: true,
  imports: [FormsModule,CommonModule,],
  templateUrl: './dashboard1.component.html',
  styleUrls: ['./dashboard1.component.css']
})
export class Dashboard1Component {

  output: string = '';
  selectedScript = '';
  today = '';
  tomorrow = '';
  year = 2025;
  week = 1;

  constructor(private scriptService: ScriptService) {}

  runScript() {
    const params: any = {};

    if (this.selectedScript === 'Create_PDF_Report/main.py') {
      params.today = this.today;
      params.tomorrow = this.tomorrow;
      
    }

    if (this.selectedScript === 'WEEKLY REPORT/main.py') {
      params.year = this.year;
      params.week = this.week;
    }

    this.scriptService.runScript(this.selectedScript, params).subscribe({
      next: (res: any) => this.output = JSON.stringify(res, null, 2),
      error: (err: any) => this.output = 'Errore: ' + JSON.stringify(err)
    });
  }
}
