import { CommonModule } from '@angular/common';
import { Component, inject, TemplateRef, ViewChild } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ChatService } from '../app/chat.service';
import { Router } from '@angular/router';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';

@Component({
  selector: 'app-test-generation',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatFormFieldModule,
  ],
  templateUrl: './test-generation.component.html',
  styleUrl: './test-generation.component.css',
})
export class TestGenerationComponent {
  @ViewChild('dialogTemplate') dialogTemplate!: TemplateRef<any>;
  featureName: string = '';
  testContext = '';
  // '{"context":"As a user, I want to log in with valid credentials so that I can access my account."}'; // User input context
  generatedTests: any[] = []; // Stores generated test scenarios
  responseTests: any[] = [];
  tempText =
    'Given that I am on the login page When I enter my valid username and password And I click on the login button Then I should be redirected to the dashboard page And I should see a welcome message with my username\n\nAs a user, I want to log in with invalid credentials so that I am notified of the error. Given that I am on the login page When I enter an invalid username or password And I click on the login button Then I should stay on the login page And I should see an error message saying "Invalid username or password"\n\nAs a user, I want to reset my password if I forget it so that I can regain access to my account. Given that I am on the login page When I click on the "Forgot Password" link Then I should be redirected to the password reset page When I enter my registered email address And I click on the "Reset Password" button Then I should receive an email with a password reset link And I should see a message saying "Please check';

  private testService = inject(ChatService); // Inject Service
  constructor(private router: Router, private matDialog: MatDialog) {}
  // Regular expression to match Given, When, Then, and And statements

  generateTests() {
    const requestBody = {
      context: this.testContext, // Wrap the input in a key named "Context"
    };
  

    // this.testService.getGeneratedTests().subscribe((tests) => {
    //   this.generatedTests = tests; // ✅ Load test cases from JSON
    // });
    // this.getFormattedTests(this.extractGivenWhenThen(this.tempText));
    //for extracting testing using open API
    this.testService.sendMessage(requestBody).subscribe((resp: any) => {
      {
        // console.log(resp['test_cases']);
        this.responseTests = this.extractGivenWhenThen(resp.test_cases);
        // this.responseTests = this.responseTests;
        console.log(this.responseTests);
        this.getFormattedTests();
      }
    });
  }

  getFormattedTests(input?: any) {
    this.responseTests.forEach((testCase) => {
      // this.extractGivenWhenThen(this.tempText).forEach((testCase) => {
      if (
        testCase.Given === '' ||
        testCase.When === '' ||
        testCase.Then === ''
      ) {
      } else {
        this.generatedTests.push({
          feature: 'Login Functionality',
          scenario: 'Successful Login with Valid Credentials',
          steps: [
            'Given ' + testCase.Given,
            'When ' + testCase.When,
            'Then ' + testCase.Then,
          ],
        });
      }
    });
  }

  extractGiven(tests: any) {}

  generateRandomID() {
    return Math.floor(1000000000 + Math.random() * 9000000000).toString();
  }

  saveTestDailog() {
    let matDialogRef = this.matDialog.open(this.dialogTemplate, {
      width: '300px',
      // data: { name: '' }, // Pass any initial data if needed
    });
    matDialogRef.afterClosed().subscribe(() => {
      this.saveTests();
      // console.log(this.featureName);
      // console.log('closedddddd');
    });
  }

  saveTests() {
    let randoemId = this.generateRandomID();
    let testScnearios: any[] = [];

    //this.extractGivenWhenThen(this.tempText)
    this.responseTests.forEach((resp) => {
      testScnearios.push({
        scenarioId: 'S001',
        scenarioName: 'Successful Login',
        scenarioDescription: 'User logs in with correct credentials',
        given: resp.Given,
        when: resp.When,
        then: resp.Then,
      });
    });

    let req = {
      featureId: randoemId,
      featureName: this.featureName, //'FeatureName-' + randoemId,
      shortDescription: 'This is new feature created by GEN AI Generator',
      featureContext: '',
      suggestedAIContextChange: '',
      state: 'Stable',
      testScenarios: testScnearios, //this.extractGivenWhenThen(this.tempText), //this.responseTests
    };
    // this.extractGiven(this.tempText);
    this.testService.saveTestFeatures(req).subscribe((resp) => {
      console.log(resp);
      this.router.navigate(['/test-update']);
    });
  }

  formatTextWithNewlines(text: any) {
    return text.replace(/\b(When|Then)\b/g, '\n$1');
  }
  extractGivenWhenThen(text: any) {
    const formattedText = this.formatTextWithNewlines(text); // Add newlines before parsing
    const matches = [
      ...formattedText.matchAll(/\b(Given|When|Then|And)\s+([^.\n]+)/g),
    ];

    const scenarios = [];
    let currentScenario = { Given: '', When: '', Then: '' };
    type Scenario = { Given: string; When: string; Then: string };
    let lastKey: keyof Scenario | null = null;

    matches.forEach((match) => {
      let keyword = match[1]; // Given, When, Then, or And
      let statement = match[2].trim();

      if (keyword === 'Given') {
        if (currentScenario.Given) {
          scenarios.push({ ...currentScenario }); // Store previous scenario
          currentScenario = { Given: '', When: '', Then: '' }; // Reset for new scenario
        }
        currentScenario.Given = statement;
        lastKey = 'Given';
      } else if (keyword === 'When') {
        if (currentScenario.When) {
          currentScenario.When += ' And ' + statement;
        } else {
          currentScenario.When = statement;
        }
        lastKey = 'When';
      } else if (keyword === 'Then') {
        if (currentScenario.Then) {
          currentScenario.Then += ' And ' + statement;
        } else {
          currentScenario.Then = statement;
        }
        lastKey = 'Then';
      } else if (keyword === 'And' && lastKey) {
        currentScenario[lastKey] += ' And ' + statement;
      }
    });

    if (currentScenario.Given) {
      scenarios.push({ ...currentScenario }); // Push the last scenario
    }

    return scenarios;
  }
}
