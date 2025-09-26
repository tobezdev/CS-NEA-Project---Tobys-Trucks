# Copilot Instructions for Toby's Trucks Stock Control System

## Project Overview
A desktop stock control system for truck retailers built with Python/Tkinter and SQLite3. This is a monolithic GUI application with a single-file architecture (`src/main.py`) managing five interconnected data tables for trucks, suppliers, customers, orders, and order items.

## Architecture Patterns

### Database Layer
- **Global Connection**: Single SQLite connection `tobysTrucksDatabase` used throughout
- **Schema**: 5 tables defined in `DB_STRUCTURES.md` - always reference this for field names/types
- **SQL Style**: Mix of f-strings and parameterized queries (parameterized preferred for new code)
- **Test Data**: Available in `DB_TESTDATA.sql` for development/testing

### GUI Architecture
- **Single Window**: `mainWindow` (Tk) with menu-driven navigation via `clearMainWindow()`
- **Global State**: All form fields use global `StringVar()` variables (e.g., `truckID`, `make`, `model`)
- **Layout**: Absolute positioning with `.place()` method, consistent color scheme (Light blue frames)
- **Assets**: Icons/images in `src/assets/` referenced via `os.path.join(assets, filename)`

### Function Naming Conventions
- **CRUD Pattern**: `list{Entity}()`, `edit{Entity}(event)`, `add{Entity}()`, `save{Entity}()`, `update{Entity}Details()`, `delete{Entity}()`
- **Forms**: `setUp{Entity}Form(heading)` for reusable form layouts
- **Selection**: `select{Entity}ToDelete()` for deletion workflows
- **Reports**: `display{ReportType}()`, `select{Entity}For{Report}()`

### Critical Patterns to Follow

#### Form Field Management
```python
# Always clear StringVar fields when creating new records
truckID.set("")
make.set("")
# Use consistent validation format labels
Label(mainWindow, bg="Light blue", text=": Format XX99").place(x=570, y=60)
```

#### Database Operations
```python
# Consistent query pattern with commit
tobysTrucksDatabase.execute("INSERT INTO truckTable VALUES (?,?,?,?,?,?,?,?,?,?)", newRecord)
tobysTrucksDatabase.commit()
# Always show user feedback
messageLabel = Label(mainWindow, font="11", bg="Light blue", text="New Truck Saved")
```

#### Event Binding Pattern
```python
# Listbox selection for editing
listTrucks.bind("<<ListboxSelect>>", editTruck)
# ComboBox selection for reports  
comboBox.bind("<<ComboboxSelected>>", displayReport)
```

## Development Workflow

### Running the Application
```bash
# From project root (uses virtual environment)
./Scripts/python -u src/main.py  # Windows
./bin/python3 -u src/main.py     # Unix
```

### File Structure
- `src/main.py` - Single monolithic application file
- `src/assets/` - GUI resources (icons, images)
- `data.db` - SQLite database (auto-created)
- `DB_STRUCTURES.md` - Database schema reference
- `DB_TESTDATA.sql` - Sample data for testing

### Known Issues & TODOs
- **Validation Missing**: Forms lack input validation (see `TODO.md`)
- **SQL Injection**: Some queries use f-strings instead of parameterized queries
- **Error Handling**: Limited database error handling in CRUD operations

## Key Integration Points
- **Menu System**: All features accessible via `setUpMainWindow()` menu bar
- **Cross-Entity References**: Trucks reference suppliers via `truckSupplierID`, orders reference customers via `orderCustomerID`
- **Reporting**: Complex queries joining multiple tables for receipts, profit reports, and order notes
- **Stock Management**: Reorder level logic triggers supplier order notes when `stockLevel <= reorderLevel`

## Code Style Guidelines
- Use consistent spacing and the existing comment header format (`#### SECTION ####`)
- Place new functions in appropriate sections (trucks, suppliers, customers, orders, reports)
- Follow the established `.place()` positioning pattern for GUI elements
- Always include user feedback messages after database operations
- Maintain the existing color scheme (Light blue frames, yellow for primary keys)

## Testing Approach
- Use `DB_TESTDATA.sql` to populate test data
- Test cross-entity relationships (supplier-truck, customer-order linkages)
- Verify menu navigation and form clearing behavior
- Test report generation with both populated and empty result sets