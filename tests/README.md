# Test Protocols

This directory contains comprehensive test protocols for Velo Supervisor 2000.

## Purpose

Test protocols document manual testing procedures to verify application functionality, business rules, and user workflows. These protocols serve as:

- **Quality Assurance**: Systematic verification of features before releases
- **Regression Testing**: Ensure existing functionality remains intact after changes
- **Documentation**: Record expected behavior and edge cases
- **Onboarding**: Help new contributors understand application behavior

## Testing Approach

Velo Supervisor 2000 uses **manual testing protocols** rather than automated tests. Each protocol provides:

1. **Test cases**: Step-by-step procedures to verify specific functionality
2. **Expected results**: What should happen when tests pass
3. **Coverage areas**: Core functionality, business rules, edge cases, error handling, UI/UX

## Available Test Protocols

- **[test_protocol_collections.md](test_protocol_collections.md)**: Comprehensive testing for the Collections feature (135 test cases)

## Future Test Protocols

As development continues, additional test protocols should be created for:

- Components management
- Bike tracking and details
- Workplans functionality
- Incident reports
- Component types
- Strava integration
- Configuration and settings

## Running Tests

1. Review the relevant test protocol document
2. Follow each test case step-by-step
3. Verify actual results match expected results
4. Document any failures or unexpected behavior
5. Create a handover document in `.handovers/` with any bugs discovered

## Contributing

When adding new features:

1. Create or update relevant test protocol
2. Document test cases covering:
   - Core functionality
   - Business rule validation
   - Edge cases and error handling
   - UI/UX behavior
3. Run through all test cases before marking feature complete
4. Reference test protocol completion in handover document

## Notes

- Test protocols are living documents - update them as features evolve
- Keep test cases clear, concise, and reproducible
- Include both positive (success) and negative (error) test cases
- Document any prerequisites or test data requirements
