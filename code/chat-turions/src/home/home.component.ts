import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  imports: [],
  standalone: true,
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  private router = inject(Router);
  startGenerating() {
    console.log('Navigating to test-generation...'); // Debugging
    this.router.navigate(['/test-generation']);
  }

  startUpdating() {
    console.log('Updating tests...');
  }

  startExecution() {
    console.log('Executing tests...');
  }
}
