import { Component } from '@angular/core';

@Component({
  selector: 'app-test-generation',
  standalone: true, 
  imports: [],
  templateUrl: './test-generation.component.html',
  styleUrl: './test-generation.component.css'
})
export class TestGenerationComponent {
  generateTests() {
    console.log('Generating tests...');
  }

  updateTests() {
    console.log('Updating tests...');
  }
}
