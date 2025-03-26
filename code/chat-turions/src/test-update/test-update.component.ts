import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../app/chat.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-test-update',
  imports: [CommonModule, FormsModule],
  templateUrl: './test-update.component.html',
  styleUrl: './test-update.component.css',
})
export class TestUpdateComponent implements OnInit {
  featureName = '';
  scenario = '';
  stepDefinition = '';

  functionalTesting = false;
  regressionTesting = false;
  performanceTesting = false;

  generatedTests: any[] = [];
  constructor(private router: Router) {}
  private testService = inject(ChatService);

  ngOnInit() {
    this.testService.getTestSuite().subscribe((tests) => {
       this.generatedTests = tests;
      console.log(tests);
    });
  }
  generateTests() {
    this.testService.getFeatureData().subscribe((tests) => {
      this.generatedTests = tests;
    });
  }

  getTest(id: any) {
    this.router.navigate(['/test-suite', id]); // Navigate and pass data via route
    console.log('Updating tests...');
  }
  getStateClass(state: string): any {
    const normalizedState = state.toLowerCase();
    return {
      'bg-green-500': normalizedState === 'stable',
      'bg-yellow-500': normalizedState === 'partially unstable',
      'bg-red-500': normalizedState === 'unstable',
    };
  }
}
